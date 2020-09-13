from baremetal import *

from assemble import *
from soc import Soc

print_debug = False
verbose = False
print_memory = False


# initialise instruction memory
with open("build/test.hex") as f:
    instructions = []
    for line in f:
        instructions.append(int(line, 16))

clk = Clock("clk")
soc = Soc(clk, 1024 * 1024, instructions)
soc.simulate(10000)
