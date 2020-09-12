import os

from baremetal import *

from assemble import *
from soc import soc

print_debug = False
verbose = False
print_memory = False


def simulate_soc(instructions, cycles):

    # create the CPU
    clk = Clock("clk")
    cpu_debug, soc_debug, output_streams = soc(clk, 1024 * 1024, instructions)

    #acknowledge all output streams
    for name, output_stream in output_streams.items():
        inp = Boolean().input(name)
        output_stream.ready.drive(inp)
        inp.set(1)

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
                # , print_instruction(cpu_debug.instruction.get())
                print("X... waiting for data")

        # debug text
        if print_debug:
            cpu_debug.display()
            soc_debug.display()

        if print_memory:

            # memory access
            if (soc_debug.data_valid.get() &
                soc_debug.data_ready.get() &
                    ~soc_debug.write_read.get()):
                print("        reading: memory[%s]" %
                      (shex(soc_debug.address.get())))
                print("             got: [%s]" %
                      (shex(soc_debug.data_in.get())))

            if (soc_debug.data_valid.get() &
                soc_debug.data_ready.get() &
                    soc_debug.write_read.get()):
                print("        writing: memory[%s]" % (
                    shex(soc_debug.address.get())),
                    "byte:", sbin(soc_debug.byte_enable.get()))
                print("             with: [%s]" %
                      (shex(soc_debug.data_out.get())))

        for name, output_stream in output_streams.items():
            if output_stream.valid.get():
                print("    output: %s: %s %x" %(
                    name, 
                    chr(output_stream.data.get()), 
                    output_stream.data.get())
                )
                if name == "debug" and output_stream.data.get() == 0x600d:
                    return True

        clk.tick()

    return False


def run_test(filename):
    # initialise instruction memory
    with open(filename) as f:
        instructions = []
        for line in f:
            instructions.append(int(line, 16))

    return simulate_soc(instructions, 10000)


for test in os.listdir("compliance_tests"):
    if test.endswith(".hex"):
        print("running", test)
        filename = os.path.join("compliance_tests", test)
        result = run_test(filename)
        if result:
            print("...pass")
        else:
            print("...fail")
