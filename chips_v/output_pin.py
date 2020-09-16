""" A bus slave that occupies a single word address provides GPIO type output
pins"""

from baremetal import *


class OutputPin:
    def __init__(self):
        self.data = Unsigned(32).wire()

    def get_outputs(self, name):
        outputs = []
        subtype = self.data.subtype
        outp = subtype.output(name + "_out", self.data)
        outputs.append(outp)
        return outputs

    def get_inputs(self, name):
        inputs = []
        return inputs


def output_pin(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    output_pin = OutputPin()
    en = slave.valid & slave.write_read
    output_pin.data = Unsigned(32).register(clk, en=en, d=slave.m2s, init=0)

    slave.s2m.drive(Unsigned(32).constant(0))
    slave.ready.drive(Boolean().constant(1))

    return output_pin
