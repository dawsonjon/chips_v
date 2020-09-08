from baremetal import *

from assemble import *
from cpu import cpu


def soc(clk, memory_size_words, memory_initial_contents):

    debug = Debug()

    # seperate initialisation data into bytes
    byte0_data = [i & 0xff for i in memory_initial_contents]
    byte1_data = [(i >> 8) & 0xff for i in memory_initial_contents]
    byte2_data = [(i >> 16) & 0xff for i in memory_initial_contents]
    byte3_data = [(i >> 24) & 0xff for i in memory_initial_contents]

    # Create byte addressable memory
    byte0 = Unsigned(8).ram(memory_size_words, clk,
                            True, initialise=byte0_data)
    byte1 = Unsigned(8).ram(memory_size_words, clk,
                            True, initialise=byte1_data)
    byte2 = Unsigned(8).ram(memory_size_words, clk,
                            True, initialise=byte2_data)
    byte3 = Unsigned(8).ram(memory_size_words, clk,
                            True, initialise=byte3_data)

    # create additional port to allow instruction reads
    byte0_insport = byte0.add_port(clk)
    byte1_insport = byte1.add_port(clk)
    byte2_insport = byte2.add_port(clk)
    byte3_insport = byte3.add_port(clk)

    # instruction port has no write access
    zero = Unsigned(32).constant(0)
    disabled = Boolean().constant(0)
    byte0_insport.write(zero, zero, disabled)
    byte1_insport.write(zero, zero, disabled)
    byte2_insport.write(zero, zero, disabled)
    byte3_insport.write(zero, zero, disabled)

    # instruction port read access
    pc = Unsigned(32).wire()
    pc_en = Boolean().wire()
    instruction_3 = byte3_insport.read(pc[31:2])
    instruction_2 = byte2_insport.read(pc[31:2])
    instruction_1 = byte1_insport.read(pc[31:2])
    instruction_0 = byte0_insport.read(pc[31:2])
    instruction = Unsigned(32).register(clk, en=pc_en, init=0, d=cat(
        instruction_3,
        instruction_2,
        instruction_1,
        instruction_0,
    ))

    debug.pc_en = pc_en
    debug.instruction = instruction
    debug.pc = pc

    # create the CPU
    data_in = Unsigned(32).register(clk, init=0)
    data_ready = Boolean().wire()
    cpu_outputs = cpu(instruction, clk, data_in, data_ready)
    (data_out, address, byte_enable, data_valid, write_read, pc_, pc_en_,
        cpu_debug) = cpu_outputs

    debug.address = address
    debug.data_out = data_out
    debug.byte_enable = byte_enable
    debug.data_valid = data_valid
    debug.write_read = write_read

    pc_en.drive(pc_en_)
    pc.drive(pc_)

    # ram write
    byte0.write(address[31:2], data_out[7:0],
                data_valid & write_read & byte_enable[0])
    byte1.write(address[31:2], data_out[15:8],
                data_valid & write_read & byte_enable[1])
    byte2.write(address[31:2], data_out[23:16],
                data_valid & write_read & byte_enable[2])
    byte3.write(address[31:2], data_out[31:24],
                data_valid & write_read & byte_enable[3])
    # write access can be accepted straight away
    write_data_ready = Boolean().constant(1)

    # ram read
    data_in.d(cat(
        byte3.read(address[31:2]),
        byte2.read(address[31:2]),
        byte1.read(address[31:2]),
        byte0.read(address[31:2])
    ))
    # read data not valid until following cycle
    read_data_ready = Boolean().register(clk, init=0)
    read_data_ready.d(data_valid & ~write_read & ~read_data_ready)

    # acknowledge data
    data_ready.drive(Boolean().select(
        write_read, read_data_ready, write_data_ready))

    debug.data_ready = data_ready
    debug.data_in = data_in

    return cpu_debug, debug
