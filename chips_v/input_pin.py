""" A bus slave that occupies a single word address provides an GPIO type
output pin"""

from baremetal import *


class InputPin:
    def __init__(self):
        self.data = Unsigned(32).wire()

    def get_inputs(self, name):
        inputs = []

        subtype = self.data.subtype
        inp = subtype.input(name + "_in")
        self.data.drive(inp)
        inputs.append(inp)

        return inputs

    def get_outputs(self, name):
        outputs = []
        return outputs


def input_pin(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    input_pin = InputPin()
    slave.s2m.drive(input_pin.data)
    slave.ready.drive(Boolean().constant(1))

    return input_pin
