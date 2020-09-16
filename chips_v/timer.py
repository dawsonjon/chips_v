""" A bus slave that occupies a single word address provides a 32 bit
system timer"""

from baremetal import *

def timer(clk, bus, from_address):
    slave = bus.add_slave(from_address, from_address+4)
    timer, last = counter(clk, 0, (2 ** 32) - 1, 1)  # 32 bit counter
    timer_hi, _ = counter(clk, 0, (2 ** 32) - 1, 1, en = last)  # 32 bit counter
    slave.ready.drive(Boolean().constant(1))
    slave.s2m.drive(Unsigned(32).select(slave.address[2], timer, timer_hi))
