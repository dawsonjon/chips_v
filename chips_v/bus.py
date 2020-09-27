"""A single master - multiple slave CPU bus for use in RISC-V CPU"""

from baremetal import *
from chips_v.utils import register


class Interconnect:
    def __init__(self):
        self.address = Unsigned(32).wire()
        self.m2s = Unsigned(32).wire()
        self.s2m = Unsigned(32).wire()
        self.ready = Boolean().wire()
        self.valid = Boolean().wire()
        self.write_read = Boolean().wire()
        self.byte_enable = Unsigned(4).wire()


class Bus:
    """ A CPU Bus"""

    def __init__(self, clk):

        self.clk = clk

        self.has_master = False
        self.address = Unsigned(32).wire()
        self.m2s = Unsigned(32).wire()
        self.valid = Boolean().wire()
        self.write_read = Boolean().wire()
        self.byte_enable = Unsigned(4).wire()

        self.s2m = Unsigned(32).constant(0)
        self.ready = Boolean().constant(0)

    def add_slave(self, block_address):
        """Connect a slave to the bus interconnect"""

        assert not self.has_master

        slave = Interconnect()

        # divide address space into 256 16Mbyte blocks.
        is_addressed = self.address[31:24] == block_address >> 24

        slave.address.drive(self.address)
        slave.m2s.drive(self.m2s)
        slave.valid.drive(self.valid & is_addressed)
        slave.write_read.drive(self.write_read)
        slave.byte_enable.drive(self.byte_enable)

        self.s2m |= self.s2m.subtype.select(
            is_addressed, Unsigned(32).constant(0), slave.s2m
        )
        self.ready |= is_addressed & slave.ready

        return slave

    def add_master(self):
        """Connect a master to the bus interconnect"""

        self.has_master = True
        master = Interconnect()

        masked_ready = Boolean().wire()

        address, m2s, valid, write_read, byte_enable = register(
            self.clk,
            Boolean().constant(1),
            master.address,
            master.m2s,
            master.valid & ~masked_ready,
            master.write_read,
            master.byte_enable,
        )
        masked_ready.drive(self.ready & valid)

        self.address.drive(address)
        self.m2s.drive(m2s)
        self.valid.drive(valid)
        self.write_read.drive(write_read)
        self.byte_enable.drive(byte_enable)

        master.s2m.drive(self.s2m)
        master.ready.drive(masked_ready)

        return master
