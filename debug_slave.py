from baremetal import *


def debug_slave(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address)
    slave.ready.drive(Boolean().constant(1))
    slave.s2m.drive(Unsigned(32).constant(0))
