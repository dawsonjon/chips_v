""" A bus slave that occupies a single word address provides an axi-like 
streaming output e.g. for connection to UART"""

from baremetal import *


class OutputStream:
    def __init__(self):
        self.data = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()

    def get_outputs(self, name):
        outputs = []
        outp = Boolean().output(name + "_valid_out", self.valid)
        outputs.append(outp)
        subtype = self.data.subtype
        outp = subtype.output(name + "_out", self.data)
        outputs.append(outp)
        return outputs

    def get_inputs(self, name):
        inputs = []
        inp = Boolean().input(name + "_ready_in")
        self.ready.drive(inp)
        inputs.append(inp)
        return inputs


def output_stream(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    output_stream = OutputStream()
    output_stream.valid = slave.valid & slave.write_read
    output_stream.data = slave.m2s

    slave.s2m.drive(Unsigned(32).constant(0))
    slave.ready.drive(output_stream.ready)

    return output_stream
