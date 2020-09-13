from baremetal import *


class InputStream:
    def __init__(self):
        self.data = Unsigned(32).wire()
        self.ready = Boolean(32).wire()
        self.valid = Boolean(32).wire()

    def connect(self, data, valid):
        self.valid.drive(valid)
        self.data.drive(data)
        return self.ready


def input_stream(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)

    input_stream = OutputStream()
    input_stream.ready = slave.valid & slave.~write_read

    slave.s2m.drive(output_stream.data)
    slave.ready.drive(output_stream.valid)

    return output_stream
