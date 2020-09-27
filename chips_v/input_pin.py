""" A bus slave that occupies a single word address provides an GPIO type
output pin"""

from baremetal import *


class InputPin:
    def __init__(self, name):
        self.data = Unsigned(32).wire()
        self.name = name

    def get_inputs(self):
        inputs = []

        subtype = self.data.subtype
        inp = subtype.input(self.name + "_in")
        self.data.drive(inp)
        inputs.append(inp)

        return inputs

    def get_outputs(self):
        outputs = []
        return outputs

    def get_declarations(self):
        """These are declarations that appear in the machine.h header"""
        return "extern const unsigned int %s;\n" % self.name

    def get_definitions(self):
        """These are declarations that appear in the machine.c definition"""
        return "const unsigned int %s = 0x%xu;\n" % (self.name, self.address)

    def initialise_sim(self):
        """in simulation terminate IO with a reasonable value"""
        self.data.drive(Unsigned(32).constant(0))

    def simulation_step(self):
        """action to perform during each simulation cycle"""
        pass

    def enumerate(self, address):
        """reserve address space"""
        self.address = address

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address)

        slave.s2m.drive(self.data)
        slave.ready.drive(Boolean().constant(1))
