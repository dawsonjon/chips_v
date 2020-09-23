""" A bus slave that occupies a single word address provides an axi-like
streaming input e.g. for connection to UART"""

from baremetal import *


class InputStream:
    def __init__(self, name):
        self.data = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()
        self.name = name

    def get_inputs(self):
        inputs = []
        inp = Boolean().input(self.name + "_valid_in")
        self.valid.drive(inp)
        inputs.append(inp)

        subtype = self.data.subtype
        inp = subtype.input(self.name + "_in")
        self.data.drive(inp)
        inputs.append(inp)
        return inputs

    def get_outputs(self):
        outputs = []
        outp = Boolean().output(self.name + "_ready_out", self.ready)
        outputs.append(outp)
        return outputs

    def initialise_sim(self):
        """in simulation terminate IO with a reasonable value"""
        self.valid.drive(Boolean().constant(1))
        self.data.drive(Boolean().constant(0))

    def simulation_step(self):
        pass

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

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address, self.address)

        self.ready = slave.valid & ~slave.write_read

        slave.s2m.drive(self.data)
        slave.ready.drive(self.valid)
