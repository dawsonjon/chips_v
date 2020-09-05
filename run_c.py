from baremetal import *
from cpu import cpu
from assemble import *
import sys
print_debug = False
verbose = False


def simulate_cpu(instructions, cycles, memory):


    #create the CPU
    clk = Clock("clk")
    data_in = Unsigned(32).input("data_in")
    data_ready = Boolean().input("data_ready")

    cpu_outputs = cpu(instructions, clk, data_in, data_ready)
    data_out, address_out, byte_enable, data_valid, write_read, debug = cpu_outputs

    #initialise the inputs
    data_ready.set(1)
    data_in.set(0)

    clk.initialise()
    for i in range(cycles):
        data_out_v, address_out_v, byte_enable_v, data_valid_v, write_read_v = (i.get() for i in cpu_outputs[:-1])

        if verbose:
            if debug.global_enable.get():  
                if debug.execute_en.get():
                    print ">... ", hex(debug.this_pc.get()),
                    print_instruction(debug.instruction.get())

                else:
                    print "X... filling"
            else:
                print "X... waiting"

        #debug text
        if print_debug:
            print ("pc", debug.pc.get(), "this_pc", debug.this_pc.get(), "fetch", debug.fetch_en.get(), "decode", debug.decode_en.get(), "execute", debug.execute_en.get(), 
                "stall", debug.stall.get(), "flush", debug.flush.get(), "take_branch", debug.take_branch.get(), "src1", shex(debug.src1.get()), "src2", shex(debug.src2.get()),
                "fwd1", debug.fwd1.get(), "fwd2", debug.fwd2.get(), "fwd_val", shex(debug.fwd_val.get()), "write_data", shex(debug.write_data.get()), "write_enable", debug.write_enable.get(),
                "data_in", shex(data_in.get()), "branch_address", shex(debug.branch_address.get()), "rd", debug.rd.get(), "rs1", debug.decoder_rs1.get(), "rs2", debug.decoder_rs2.get())


        #memory access
        if data_valid_v:
            if write_read_v==0:
                print "        read: data_in <= memory[%s]"%(shex(address_out_v)) , "byte:", sbin(byte_enable_v)
                #read memory
                if address_out_v is None:
                    data_in.set(None)
                else:
                    data_in.set(memory.get(address_out_v >> 2, 0))
                print "        read data: %s"%(shex(data_in.get()))

        clk.tick()

        #memory access
        if data_valid_v:
            if write_read_v:
                print "        write: memory[%s] <= %s"%(shex(address_out_v), shex(data_out_v)), "byte:", sbin(byte_enable_v) 
                if address_out_v == 0x12345678:
                    print chr(data_out_v & 0xff)
                #write memory
                data = memory.get(address_out_v, 0)
                if data_out_v is None:
                    data_out_v = 0
                if byte_enable_v & 1:
                    data = (data & 0xffffff00) | (data_out_v & 0x000000ff)
                if byte_enable_v & 2:
                    data = (data & 0xffff00ff) | (data_out_v & 0x0000ff00)
                if byte_enable_v & 4:
                    data = (data & 0xff00ffff) | (data_out_v & 0x00ff0000)
                if byte_enable_v & 8:
                    data = (data & 0x00ffffff) | (data_out_v & 0xff000000)
                memory[address_out_v >> 2] = data

    return memory

#initialise instruction memory
with open("build/test_ins.hex") as f:
    instructions = []
    for line in f:
        instructions.append(int(line, 16))

#initialise instruction memory
memory = {}
with open("build/test_mem.hex") as f:
    address = 0x100
    for line in f:
        memory[address] = (int(line, 16))
        address += 1
print instructions
for address in sorted(memory.keys()):
    data = memory[address]
    print shex(address*4), shex(memory[address]), chr(data >> 24 & 0xff), chr(data >> 16 & 0xff), chr(data >> 8 & 0xff), chr(data >> 0 & 0xff)
memory = simulate_cpu(instructions, 400, memory)
