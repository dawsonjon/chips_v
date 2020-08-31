from baremetal import *
from utils import *
from decode import decode
from execute import execute

def cpu(instructions, clk, data_in, data_ready):

    global fetch_en
    global decode_en
    global execute_en
    global this_pc
    global fetched_instruction
    global instruction
    global flush
    global stall
    global take_branch
    global src1
    global src2
    global fwd1
    global fwd2
    global fwd_val
    global write_data
    global write_enable
    global rd
    global global_enable
    global branch_address
    global pc

    #generate a global enable signal
    stall = Boolean().wire()
    global_enable = ~stall

    #simple state machine to control pipeline
    flush = Boolean().wire()
    fetch_en   = Boolean().constant(1)
    decode_en  = Boolean().register(clk, en=global_enable, init=0, d=fetch_en & ~flush)
    execute_en = Boolean().register(clk, en=global_enable, init=0, d=decode_en & ~flush)

    ############################################################################# 
    # Fetch - pipeline stage 0
    ############################################################################# 

    pc = Unsigned(32).register(clk, init=0, en=fetch_en & global_enable)
    instruction = Unsigned(32).rom(pc>>2, *instructions)
    instruction, this_pc = register(clk, fetch_en & global_enable, instruction, pc)

    fetched_instruction = instruction

    ############################################################################# 

                                    ###

    ############################################################################# 
    # Decode - pipeline stage 1
    ############################################################################# 

    #read registers
    decoder_rs1 = instruction[19:15]
    decoder_rs2 = instruction[24:20]
    registersa = Signed(32).ram(clk=clk, depth=32)
    registersb = Signed(32).ram(clk=clk, depth=32)
    src1 = registersa.read(decoder_rs1)
    src2 = registersb.read(decoder_rs2)

    #decode instruction
    fwd1 = Boolean().wire()
    fwd2 = Boolean().wire()
    fwd_val = Signed(32).wire()
    decode_outputs = decode(instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc)
    decode_outputs += (instruction, this_pc)

    #register outputs
    decode_outputs = register(clk, global_enable & decode_en, *decode_outputs)
    (src1, src2, A, B, operation, shift_amount, add_sub, signed, instruction, this_pc) = decode_outputs

    ############################################################################# 

                                    ###

    ############################################################################# 
    # Execute - pipeline stage 2
    ############################################################################# 

    #execute instruction
    execute_outputs = execute(instruction, src1, src2, A, B, operation, add_sub, shift_amount, signed, data_in, this_pc)
    (write_data, write_enable, data_out, address_out, byte_enable, data_valid, write_read, take_branch, branch_address) = execute_outputs

    #write registers
    rd = instruction[11:7]
    registersa.write(rd, write_data, write_enable & execute_en & global_enable)
    registersb.write(rd, write_data, write_enable & execute_en & global_enable)

    #register forwarding
    fwd1.drive(decoder_rs1 == rd & write_enable & execute_en & global_enable)
    fwd2.drive(decoder_rs2 == rd & write_enable & execute_en & global_enable)
    fwd_val.drive(write_data)

    ############################################################################# 

    # Increment Program Counter
    pc.d(Unsigned(32).select(take_branch & execute_en, pc+4, branch_address))
    flush.drive(execute_en & take_branch)

    #stall the whole pipeline if we are waiting for some event before we continue
    stall.drive(execute_en & data_valid & ~data_ready) #|go and ~done


    return data_out, address_out, byte_enable, data_valid, write_read

def build_cpu(instructions):

    clk = Clock("clk")
    data_in = Unsigned(32).input("data_in")
    data_ready = Boolean().input("data_ready")

    cpu_outputs = cpu(instructions, clk, data_in, data_ready)
    data_out, address_out, byte_enable, data_valid, write_read = cpu_outputs

    data_out = Unsigned(32).output("data_out", data_out)
    address = Unsigned(32).output("address", address_out)
    byte_enable = Unsigned(4).output("byte_enable", byte_enable)
    data_valid = Boolean().output("data_valid", data_valid)
    write_read = Boolean().output("write_read", write_read)

    netlist = Netlist(
        "cpu",
        [clk], 
        [data_in, data_ready],
        [data_out, address, byte_enable, data_valid, write_read],
    )
    f = open("cpu.v", "w")
    f.write(netlist.generate())


if __name__ == "__main__":
    import sys

    if "simulate" in sys.argv:

        from assemble import *

        instructions = [
            addi(result_reg=1, immediate = 0x1, reg=0), #initialise to 0
            addi(result_reg=1, immediate = 0x1, reg=1), #add 1
            sw(address_offset=0, address_reg=0, data_reg=1), #output
            jal(immediate=-8, result_reg=0, reg=0) #go back 2 instructions
        ]

        data_values = [0x12345678, 0x12345678, 0x12345678, 0x12345678, 0x12345678]
        data_values = iter(data_values)

        clk = Clock("clk")
        data_in = Unsigned(32).input("data_in")
        data_ready = Boolean().input("data_ready")

        cpu_outputs = cpu(instructions, clk, data_in, data_ready)
        data_out, address_out, byte_enable, data_valid, write_read = cpu_outputs

        data_ready.set(1)
        data_in.set(data_values.next())

        clk.initialise()
        for i in range(20):


            #print ("pc", pc.get(), "this_pc", this_pc.get(), "fetch", fetch_en.get(), "decode", decode_en.get(), "execute", execute_en.get(), 
                    #"stall", stall.get(), "flush", flush.get(), "take_branch", take_branch.get(), "src1", shex(src1.get()), "src2", shex(src2.get()),
                    #"fwd1", fwd1.get(), "fwd2", fwd2.get(), "fwd_val", shex(fwd_val.get()), "write_data", shex(write_data.get()), "write_enable", write_enable.get(),
                    #"data_in", shex(data_in.get()), "branch_address", shex(branch_address.get()))
            data_out_v, address_out_v, byte_enable_v, data_valid_v, write_read_v = (i.get() for i in cpu_outputs)

            if global_enable.get():  
                if execute_en.get():
                    print ">... ", this_pc.get(),
                    print_instruction(instruction.get())

                    if data_valid_v == 1:
                        if write_read_v:
                            print "        write: memory[%s] <= %s"%(shex(address_out_v), shex(data_out_v)), "byte:", sbin(byte_enable_v) 
                        else:
                            print "        read: data_in <= memory[%s] == %s"%(shex(address_out_v), shex(data_in.get())) , "byte:", sbin(byte_enable_v)

                else:
                    print "X... filling"
            else:
                print "X... waiting"


            clk.tick()

            if data_valid_v & data_ready.get() & ~write_read.get():
                data_in.set(data_values.next())

    if "build" in sys.argv:
        from assemble import *
        instructions = [
            addi(result_reg=1, immediate = 0x1, reg=0),
            sw(address_offset=0, address_reg=0, data_reg=1),
            addi(result_reg=1, immediate = 0x1, reg=1),
            sw(address_offset=0, address_reg=0, data_reg=1),
            addi(result_reg=1, immediate = 0x1, reg=1),
            sw(address_offset=0, address_reg=0, data_reg=1),
        ]
        build_cpu(instructions)
