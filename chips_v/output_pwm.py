""" A bus slave that occupies a single word address provides PWM output pins"""

from baremetal import *
from chips_v.pwm import pwm


class OutputPWM:
    def __init__(self, name, clock_frequency, output_frequency, bits):
        self.name = name
        self.clock_frequency = clock_frequency
        self.output_frequency = output_frequency
        self.bits = bits

    def get_outputs(self):
        outputs = []
        subtype = self.pwm.subtype
        outp = subtype.output(self.name + "_pwm_out", self.pwm)
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
        self.pwm = pwm(
            clk, slave.m2s, en, self.clock_frequency, self.output_frequency, self.bits
        )

        slave.s2m.drive(Unsigned(32).constant(0))
        slave.ready.drive(Boolean().constant(1))

        self.data_valid = en
        self.debug_data = slave.m2s
