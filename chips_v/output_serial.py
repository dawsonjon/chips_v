""" A bus slave that occupies a single word address provides a UART output interface"""

from baremetal import *

from chips_v.serial import serial_out


class OutputSerial:
    def __init__(self, name, clock_rate, baud_rate):
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate

    def get_outputs(self):
        outputs = []
        outp = Boolean().output(self.name + "_tx", self.tx)
        outputs.append(outp)
        return outputs

    def get_inputs(self):
        inputs = []
        return inputs

    def get_declarations(self):
        """These are declarations that appear in the machine.h header"""
        return "extern const unsigned int %s;\n" % self.name

    def get_definitions(self):
        """These are declarations that appear in the machine.c definition"""
        return "const unsigned int %s = 0x%xu;\n" % (self.name, self.address)

    def enumerate(self, address):
        """reserve address space"""
        self.address = address
        return address + 4

    def initialise_sim(self):
        """in simulation terminate IO with a reasonable value"""
        pass

    def simulation_step(self):
        """action to perform during each simulation cycle"""
        if self.debug.idle.get() and self.debug.tx_valid.get():
            print(
                "Serial Output %s writing %s" % (self.name, self.debug.input_data.get())
            )

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address, self.address)

        tx_ready, tx, self.debug = serial_out(
            clk,
            slave.m2s[7:0],
            slave.valid & slave.write_read,
            self.clock_rate,
            self.baud_rate,
        )

        self.tx = tx

        slave.s2m.drive(Unsigned(32).constant(0))
        slave.ready.drive(tx_ready)
