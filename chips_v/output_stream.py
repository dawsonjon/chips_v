""" A bus slave that occupies a single word address provides an axi-like 
streaming output e.g. for connection to UART"""

from baremetal import *
from chips_v.utils import shex


class OutputStream:
    def __init__(self, name):
        self.data = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()
        self.name = name

    def get_outputs(self):
        outputs = []
        outp = Boolean().output(self.name + "_valid_out", self.valid)
        outputs.append(outp)
        subtype = self.data.subtype
        outp = subtype.output(self.name + "_out", self.data)
        outputs.append(outp)
        return outputs

    def get_inputs(self):
        inputs = []
        inp = Boolean().input(self.name + "_ready_in")
        self.ready.drive(inp)
        inputs.append(inp)
        return inputs

    def initialise_sim(self):
        """in simulation terminate IO with a reasonable value"""
        self.ready.drive(Boolean().constant(1))

    def simulation_step(self):
        """action to perform during each simulation cycle"""
        if self.ready.get() and self.valid.get():
            print(
                "OutputStream %s writing: %s %s %s"
                % (
                    self.name,
                    self.data.get(),
                    shex(self.data.get()),
                    chr(self.data.get() & 0xFF),
                )
            )

    def get_declarations(self):
        """These are declarations that appear in the machine.h header"""
        return "extern const unsigned int %s;\n" % self.name

    def get_definitions(self):
        """These are declarations that appear in the machine.c definition"""
        return "const unsigned int %s = 0x%xu;\n" % (self.name, self.address)

    def enumerate(self, address):
        """reserve address space"""
        self.address = address

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address)

        self.valid = slave.valid & slave.write_read
        self.data = slave.m2s

        slave.s2m.drive(Unsigned(32).constant(0))
        slave.ready.drive(self.ready)
