""" A bus slave that occupies a single word address provides GPIO type output
pins"""

from baremetal import *


class OutputPin:
    def __init__(self, name):
        self.data = Unsigned(32).wire()
        self.name = name

    def get_outputs(self):
        outputs = []
        subtype = self.data.subtype
        outp = subtype.output(self.name + "_out", self.data)
        outputs.append(outp)
        return outputs

    def get_inputs(self):
        inputs = []
        return inputs

    def get_declarations(self):
        """These are declarations that appear in the machine.h header"""
        return "extern const unsigned int %s;\n" % self.name

    def get_definitions(self):
        """These are declarations that appear in the machine.c definition"""
        return "const unsigned int %s = 0x%xu;\n" % (self.name, self.address)

    def enumerate(self, address):
        """reserve address space"""
        self.address = address
        return address + 4

    def initialise_sim(self):
        """in simulation terminate IO with a reasonable value"""
        pass

    def simulation_step(self):
        """action to perform during each simulation cycle"""
        if self.data_valid.get():
            print("Output pin %s writing %s" % (self.name, self.debug_data.get()))

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address, self.address)

        en = slave.valid & slave.write_read
        self.data = Unsigned(32).register(clk, en=en, d=slave.m2s, init=0)

        slave.s2m.drive(Unsigned(32).constant(0))
        slave.ready.drive(Boolean().constant(1))

        self.data_valid = en
        self.debug_data = slave.m2s
