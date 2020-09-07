from baremetal import *
from soc import soc
from assemble import *
import sys
print_debug = False
verbose = False
print_memory = False


def simulate_soc(instructions, cycles):

    #create the CPU
    clk = Clock("clk")
    cpu_debug, soc_debug = soc(clk, 1024*1024, instructions)

    clk.initialise()
    for i in range(cycles):

        if verbose:
            if cpu_debug.global_enable.get():  
                if cpu_debug.execute_en.get():
                    print ">... ", hex(cpu_debug.this_pc.get()),
                    print_instruction(cpu_debug.instruction.get())

                else:
                    print "X... filling"
            else:
                print "X... waiting for data", print_instruction(cpu_debug.instruction.get())

        #debug text
        if print_debug:
            cpu_debug.display()
            soc_debug.display()

        if print_memory:

            #memory access
            if soc_debug.data_valid.get() & soc_debug.data_ready.get() & ~soc_debug.write_read.get():
                print "        reading: memory[%s]"%(shex(soc_debug.address.get()))
                print "             got: [%s]"%(shex(soc_debug.data_in.get()))

            if soc_debug.data_valid.get() & soc_debug.data_ready.get() & soc_debug.write_read.get():
                print "        writing: memory[%s]"%(shex(soc_debug.address.get())) , "byte:", sbin(soc_debug.byte_enable.get())
                print "             with: [%s]"%(shex(soc_debug.data_out.get()))

        if soc_debug.data_valid.get() & soc_debug.data_ready.get() & soc_debug.write_read.get():
            if soc_debug.address.get() == 0x12345678:
                print "         debug: %s"%hex(soc_debug.data_out.get())
                if soc_debug.data_out.get() == 0x600d:
                    print "pass"
                    sys.exit(1)
                else:
                    print "fail"
                    sys.exit(0)


        clk.tick()

#initialise instruction memory
with open("compliance_tests/test.hex") as f:
    instructions = []
    for line in f:
        instructions.append(int(line, 16))

memory = simulate_soc(instructions, 10000)
