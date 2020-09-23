""" A bus slave that occupies a single word address provides a UART input """

from baremetal import *

from chips_v.serial import serial_in


class InputSerial:
    def __init__(self, name, clock_rate, baud_rate):
        self.rx = Boolean().wire()
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate

    def get_inputs(self):
        inputs = []
        inp = Boolean().input(self.name + "_rx")
        self.rx.drive(inp)
        inputs.append(inp)
        return inputs

    def get_outputs(self):
        outputs = []
        return outputs

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
        self.rx.drive(Unsigned(32).constant(1))

    def simulation_step(self):
        """action to perform during each simulation cycle"""
        pass

    def attach(self, clk, bus):
        slave = bus.add_slave(self.address, self.address)

        rx_valid, rx_data, debug = serial_in(
            clk,
            self.rx,
            slave.valid & ~slave.write_read,
            self.clock_rate,
            self.baud_rate,
        )
        slave.s2m.drive(rx_data.resize(32))
        slave.ready.drive(rx_valid)
