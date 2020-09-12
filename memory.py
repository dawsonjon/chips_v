from baremetal import *


def create_soc_memory(clk, memory_initial_contents, memory_size_words,
                      pc, pc_en, bus):

    slave = bus.add_slave(0, (memory_size_words * 4) - 4)

    # Separate initialisation data into bytes
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

    # Connect RAM to CPU bus
    byte0.write(slave.address[31:2], slave.m2s[7:0],
                slave.valid & slave.write_read & slave.byte_enable[0])
    byte1.write(slave.address[31:2], slave.m2s[15:8],
                slave.valid & slave.write_read & slave.byte_enable[1])
    byte2.write(slave.address[31:2], slave.m2s[23:16],
                slave.valid & slave.write_read & slave.byte_enable[2])
    byte3.write(slave.address[31:2], slave.m2s[31:24],
                slave.valid & slave.write_read & slave.byte_enable[3])

    # write access can be accepted straight away
    write_data_ready = Boolean().constant(1)

    # ram read
    memory_s2m = Unsigned(32).register(clk, init=0)
    memory_s2m.d(cat(
        byte3.read(slave.address[31:2]),
        byte2.read(slave.address[31:2]),
        byte1.read(slave.address[31:2]),
        byte0.read(slave.address[31:2])
    ))
    slave.s2m.drive(memory_s2m)

    # read data not valid until following cycle
    read_data_ready = Boolean().register(clk, init=0)
    read_data_ready.d(slave.valid & ~slave.write_read & ~read_data_ready)

    # acknowledge data
    slave.ready.drive(Boolean().select(
        slave.write_read, read_data_ready, write_data_ready))

    return instruction
