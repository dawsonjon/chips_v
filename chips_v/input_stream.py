""" A bus slave that occupies a single word address provides an axi-like
streaming input e.g. for connection to UART"""

from baremetal import *


class InputStream:
    def __init__(self):
        self.data = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()

    def get_inputs(self, name):
        inputs = []
        inp = Boolean().input(name + "_valid_in")
        self.valid.drive(inp)
        inputs.append(inp)

        subtype = self.data.subtype
        inp = subtype.input(name + "_in")
        self.data.drive(inp)
        inputs.append(inp)
        return inputs

    def get_outputs(self, name):
        outputs = []
        outp = Boolean().output(name + "_ready_out", self.ready)
        outputs.append(outp)
        return outputs


def input_stream(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    input_stream = InputStream()
    input_stream.ready = slave.valid & ~slave.write_read

    slave.s2m.drive(input_stream.data)
    slave.ready.drive(input_stream.valid)

    return input_stream
