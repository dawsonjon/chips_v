from baremetal import *


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

    def __init__(self):
        self.has_master = False
        self.address = Unsigned(32).wire()
        self.m2s = Unsigned(32).wire()
        self.s2m = Unsigned(32).constant(0)
        self.ready = Boolean().constant(0)
        self.valid = Boolean().wire()
        self.write_read = Boolean().wire()
        self.byte_enable = Unsigned(4).wire()

    def add_slave(self, from_address, to_address):
        """Connect a slave to the bus interconnect"""

        assert not self.has_master

        slave = Interconnect()

        is_addressed = (
            (self.address >= from_address) & (self.address <= to_address)
        )

        slave.address.drive(self.address)
        slave.m2s.drive(self.m2s)
        slave.valid.drive(self.valid & is_addressed)
        slave.write_read.drive(self.write_read)
        slave.byte_enable.drive(self.byte_enable)

        self.s2m = self.s2m.subtype.select(is_addressed, self.s2m, slave.s2m)
        self.ready = Boolean().select(is_addressed, self.ready, slave.ready)

        return slave

    def add_master(self):
        """Connect a master to the bus interconnect"""

        self.has_master = True
        master = Interconnect()
        self.address.drive(master.address)
        self.m2s.drive(master.m2s)
        self.valid.drive(master.valid)
        self.write_read.drive(master.write_read)
        self.byte_enable.drive(master.byte_enable)
        master.s2m.drive(self.s2m)
        master.ready.drive(self.ready)

        return master
