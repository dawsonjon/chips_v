""" A bus slave that occupies a single word address provides a UART output interface"""

from baremetal import *

from chips_v.serial import serial_out


class OutputSerial:
    def get_outputs(self, name):
        outputs = []
        outp = Boolean().output(name + "_tx", self.tx)
        outputs.append(outp)
        return outputs

    def get_inputs(self, name):
        inputs = []
        return inputs


def output_serial(clk, bus, from_address, clk_rate, baud_rate):
    slave = bus.add_slave(from_address, from_address)

    tx_ready, tx, _ = serial_out(
        clk, slave.m2s[7:0], slave.valid & slave.write_read, clk_rate, baud_rate
    )

    output_stream = OutputSerial()
    output_stream.tx = tx

    slave.s2m.drive(Unsigned(32).constant(0))
    slave.ready.drive(tx_ready)

    return output_stream
