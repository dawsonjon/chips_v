from baremetal import *


class OutputStream:
    def __init__(self):
        self.data = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()

    def connect(self,  ready):
        self.ready.driver(ready)
        return self.data, self.valid


def output_stream(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    output_stream = OutputStream()
    output_stream.valid = slave.valid & slave.write_read
    output_stream.data = slave.m2s

    slave.s2m.drive(Unsigned(32).constant(0))
    slave.ready.drive(output_stream.ready)

    return output_stream
