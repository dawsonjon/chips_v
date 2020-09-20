""" A bus slave that occupies a single word address provides an UART input """

from baremetal import *


class InputStream:
    def __init__(self):
        self.rx = Boolean().wire()

    def get_inputs(self, name):
        inputs = []
        inp = Boolean().input(name)
        self.rx.drive(inp)
        inputs.append(inp)
        return inputs

    def get_outputs(self, name):
        outputs = []
        return outputs


def input_stream(clk, bus, from_address, clk_rate, baud_rate):
    input_stream = InputStream()

    slave = bus.add_slave(from_address, from_address)

    rx_data, rx_valid, _ = serial_in(clk, input_stream.rx, slave.valid & ~slave.write_read, clk_rate, baud_rate)
    slave.s2m.drive(rx_data)
    slave.ready.drive(rx_valid)


    return input_stream
