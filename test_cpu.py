from baremetal import *
from cpu import cpu
from assemble import *
import sys
print_debug = True
verbose = True


def simulate_cpu(instructions, cycles):


    #create the CPU
    clk = Clock("clk")
    data_in = Unsigned(32).input("data_in")
    data_ready = Boolean().input("data_ready")

    cpu_outputs = cpu(instructions, clk, data_in, data_ready)
    data_out, address_out, byte_enable, data_valid, write_read, debug = cpu_outputs

    #initialise the inputs
    data_ready.set(1)
    data_in.set(0)
    memory = {}

    clk.initialise()
    for i in range(cycles):
        data_out_v, address_out_v, byte_enable_v, data_valid_v, write_read_v = (i.get() for i in cpu_outputs[:-1])


        if verbose:
            if debug.global_enable.get():  
                if debug.execute_en.get():
                    print ">... ", debug.this_pc.get(),
                    print_instruction(debug.instruction.get())

                    if data_valid_v == 1:
                        if write_read_v:
                            print "        write: memory[%s] <= %s"%(shex(address_out_v), shex(data_out_v)), "byte:", sbin(byte_enable_v) 
                        else:
                            print "        read: data_in <= memory[%s] == %s"%(shex(address_out_v), shex(data_in.get())) , "byte:", sbin(byte_enable_v)

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


        clk.tick()

        #memory access
        if data_valid_v:
            if write_read_v:
                #write memory
                data = memory.get(address_out_v, 0)
                print data, data_out_v
                if byte_enable_v & 1:
                    data = (data & 0xffffff00) | (data_out_v & 0x000000ff)
                if byte_enable_v & 2:
                    data = (data & 0xffff00ff) | (data_out_v & 0x0000ff00)
                if byte_enable_v & 4:
                    data = (data & 0xff00ffff) | (data_out_v & 0x00ff0000)
                if byte_enable_v & 8:
                    data = (data & 0x00ffffff) | (data_out_v & 0xff000000)
                print address_out_v>>2, data
                memory[address_out_v >> 2] = data
                print memory
            else:
                #read memory
                if address_out_v is None:
                    data_in.set(None)
                else:
                    data_in.set(memory[address_out_v >> 2])
        #print "memory", memory

    return memory


#walking ones across data bus
instructions = [
    addi(result_reg=1, immediate = 0x00000001, reg=0),
    addi(result_reg=2, immediate = 0x00000000, reg=0),
    addi(result_reg=3, immediate = 32, reg=0),
    sw(address_offset=0, address_reg=2, data_reg=1),
    add(result_reg=1, reg2=1, reg=1),
    addi(result_reg=2, immediate = 4, reg=2),
    addi(result_reg=3, immediate = -1, reg=3),
    bne(immediate=-16, reg=3, reg2=0),
    jal(immediate=0, result_reg=0) #infinite loop
]
memory = simulate_cpu(instructions, 300)
for address in sorted(memory.keys()):
    print shex(address*4), shex(memory[address])

#walking ones across address bus
instructions = [
    addi(result_reg=1, immediate = 0x00000004, reg=0),
    addi(result_reg=2, immediate = 0x00000000, reg=0),
    addi(result_reg=3, immediate = 30, reg=0),
    sw(address_offset=0, address_reg=1, data_reg=2),
    add(result_reg=1, reg2=1, reg=1),
    addi(result_reg=2, immediate = 1, reg=2),
    addi(result_reg=3, immediate = -1, reg=3),
    bne(immediate=-16, reg=3, reg2=0),
    jal(immediate=0, result_reg=0) #infinite loop
]
memory = simulate_cpu(instructions, 250)
for address in sorted(memory.keys()):
    print shex(address*4), shex(memory[address])


#instructions = [
    #addi(result_reg=1, immediate = 0x1, reg=0), #initialise to 0
    #addi(result_reg=1, immediate = 0x1, reg=1), #add 1
    #sw(address_offset=0, address_reg=0, data_reg=1), #output
    ##jal(immediate=-8, result_reg=0) #go back 2 instructions
    #auipc(immediate=0, result_reg=31), #go back 2 instructions
    #jalr(immediate=-8, result_reg=0, reg=31) #go back 2 instructions
#]


