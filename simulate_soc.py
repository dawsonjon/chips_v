import sys

from assemble import *
from baremetal import *
from soc import soc

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
                    print(">... ", hex(cpu_debug.this_pc.get()), end=' ')
                    print_instruction(cpu_debug.instruction.get())

                else:
                    print("X... filling")
            else:
                print("X... waiting for data", print_instruction(cpu_debug.instruction.get()))

        #debug text
        if print_debug:
            cpu_debug.display()
            soc_debug.display()

        if print_memory:

            #memory access
            if soc_debug.data_valid.get() & soc_debug.data_ready.get() & ~soc_debug.write_read.get():
                print("        reading: memory[%s]"%(shex(soc_debug.address.get())))
                print("             got: [%s]"%(shex(soc_debug.data_in.get())))

            if soc_debug.data_valid.get() & soc_debug.data_ready.get() & soc_debug.write_read.get():
                print("        writing: memory[%s]"%(shex(soc_debug.address.get())) , "byte:", sbin(soc_debug.byte_enable.get()))
                print("             with: [%s]"%(shex(soc_debug.data_out.get())))

        if soc_debug.data_valid.get() & soc_debug.data_ready.get() & soc_debug.write_read.get():
            if soc_debug.address.get() == 0x12345678:
                print("         debug: %s"%chr(soc_debug.data_out.get()))


        clk.tick()

#initialise instruction memory
with open("build/test.hex") as f:
    instructions = []
    for line in f:
        instructions.append(int(line, 16))

print(instructions)

memory = simulate_soc(instructions, 10000)
