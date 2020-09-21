""" A bus slave that occupies a single word address provides a UART input """

from baremetal import *

from chips_v.serial import serial_in


class InputSerial:
    def __init__(self):
        self.rx = Boolean().wire()

    def get_inputs(self, name):
        inputs = []
        inp = Boolean().input(name + "_rx")
        self.rx.drive(inp)
        inputs.append(inp)
        return inputs

    def get_outputs(self, name):
        outputs = []
        return outputs


def input_serial(clk, bus, from_address, clk_rate, baud_rate):
    input_stream = InputSerial()

    slave = bus.add_slave(from_address, from_address)

    rx_valid, rx_data, debug = serial_in(
        clk, input_stream.rx, slave.valid & ~slave.write_read, clk_rate, baud_rate
    )
    slave.s2m.drive(rx_data.resize(32))
    slave.ready.drive(rx_valid)

    debug.slave_ready = slave.ready
    debug.slave_rx_valid = rx_valid
    debug.slave_s2m = slave.s2m

    return input_stream, debug
