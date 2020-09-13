from baremetal import *


def timer(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address+4)
    timer, _ = counter(clk, 0, (2 ** 64) - 1, 1)  # 32 bit counter
    slave.ready.drive(Boolean().constant(1))
    slave.s2m.drive(Unsigned(32).select(slave.address[2], timer[31:0], timer[63:32]))
