""" A bus slave that occupies a single word address provides an axi-like 
streaming output e.g. for connection to UART"""

from baremetal import *


class OutputStream:

    def get_outputs(self, name):
        outputs = []
        outp = Boolean().output(name + "_valid_out", self.tx)
        outputs.append(outp)
        return outputs

    def get_inputs(self, name):
        inputs = []
        return inputs


def output_stream(clk, bus, from_address, clk_rate, baud_rate):
    slave = bus.add_slave(from_address, from_address)

    tx_ready, tx, _ = serial_out(clk, slave.s2m, slave.valid & slave.write_read, clk_rate, baud_rate)

    output_stream = OutputStream()
    output_stream.tx = tx

    slave.s2m.drive(Unsigned(32).constant(0))
    slave.ready.drive(tx_ready)

    return output_stream
