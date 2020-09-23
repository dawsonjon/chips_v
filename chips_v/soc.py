"""A configurable RISC-V SoC with hardware generation and simulation capability"""

import os

import chips_v.input_stream
import chips_v.output_stream
import chips_v.input_pin
import chips_v.output_pin
import chips_v.input_serial
import chips_v.output_serial
from baremetal import *
from chips_v.bus import Bus
from chips_v.cpu import cpu
from chips_v.default_spec import default_settings
from chips_v.memory import create_soc_memory
from chips_v.timer import timer
from chips_v.utils import *


class Soc:
    def __init__(
        self, clk, memory_size_words, memory_initial_contents, settings=default_settings
    ):

        self.clk = clk

        debug = Debug()
        self.peripherals = settings["peripherals"]

        # create a bus
        bus = Bus()

        # connect slaves to bus
        pc = Unsigned(32).wire()
        pc_en = Boolean().wire()
        instruction = create_soc_memory(
            clk, memory_initial_contents, memory_size_words, pc, pc_en, bus
        )

        # timer
        timer(clk, bus, 0x80000000)

        # output_streams
        for peripheral in self.peripherals:
            peripheral.attach(clk, bus)

        # create the CPU
        pc_, pc_en_, cpu_debug = cpu(instruction, clk, bus, settings["march"])
        pc_en.drive(pc_en_)
        pc.drive(pc_)

        # connect up signals for debug
        debug.address = bus.address
        debug.data_valid = bus.valid
        debug.data_ready = bus.ready
        debug.write_read = bus.write_read
        debug.byte_enable = bus.byte_enable
        debug.data_out = bus.m2s
        debug.data_in = bus.s2m

        self.cpu_debug = cpu_debug
        self.soc_debug = debug

    def simulate(self, cycles, print_debug=False, verbose=False, print_memory=False):

        cpu_debug = self.cpu_debug
        soc_debug = self.soc_debug

        # acknowledge all output streams
        for peripheral in self.peripherals:
            peripheral.initialise_sim()

        self.clk.initialise()
        elapsed = 0
        while 1:

            if verbose:
                if cpu_debug.global_enable.get():
                    if cpu_debug.execute_en.get():
                        print(">... ", hex(cpu_debug.this_pc.get()), end=" ")
                        print_instruction(cpu_debug.instruction.get())

                    else:
                        print("X... filling")
                else:
                    print(
                        "X... waiting for data",
                        print_instruction(cpu_debug.instruction.get()),
                        print_instruction(soc_debug.address.get()),
                    )

            # debug text
            if print_debug:
                cpu_debug.display()
                soc_debug.display()

            if print_memory:
                # memory access
                if (
                    soc_debug.data_valid.get()
                    & soc_debug.data_ready.get()
                    & ~soc_debug.write_read.get()
                ):
                    print(
                        "        reading: memory[%s]" % (shex(soc_debug.address.get()))
                    )
                    print("             got: [%s]" % (shex(soc_debug.data_in.get())))

                if (
                    soc_debug.data_valid.get()
                    & soc_debug.data_ready.get()
                    & soc_debug.write_read.get()
                ):
                    print(
                        "        writing: memory[%s]" % (shex(soc_debug.address.get())),
                        "byte:",
                        sbin(soc_debug.byte_enable.get()),
                        soc_debug.address.get() / 16,
                    )
                    print("             with: [%s]" % (shex(soc_debug.data_out.get())))

            for peripheral in self.peripherals:
                peripheral.simulation_step()

            # in compliance text monitor writes to a specific address to determine pass/fail
            if (
                soc_debug.data_valid.get()
                & soc_debug.data_ready.get()
                & soc_debug.write_read.get()
            ):
                if soc_debug.address.get() == 0x80000008:
                    if soc_debug.data_out.get() == 0xBAD:
                        return False
                    if soc_debug.data_out.get() == 0x600D:
                        return True

            # print out stream outputs, ignore pins
            try:
                # stop simulation if infinite loop encountered
                if cpu_debug.global_enable.get():
                    if cpu_debug.execute_en.get():
                        if cpu_debug.take_branch.get():
                            if (
                                cpu_debug.this_pc.get()
                                == cpu_debug.branch_address.get()
                            ):
                                print("cpu halted")
                                return True
            except AttributeError:
                pass

            self.clk.tick()

            if cycles and elapsed >= cycles:
                print("Simulation timed out")
                return False

            elapsed += 1

    def generate_verilog(self, netlist_name):

        # Sanitise netlist name
        if not netlist_name.isidentifier():
            netlist_name = os.path.basename(netlist_name)
            netlist_name = os.path.splitext(netlist_name)[0]

        inputs = []
        outputs = []
        # Populate a list of inputs and outputs
        for peripheral in self.peripherals:
            inputs.extend(peripheral.get_inputs())
            outputs.extend(peripheral.get_outputs())

        # Generate verilog netlist
        netlist = Netlist(netlist_name, [self.clk], inputs, outputs)
        f = open(netlist_name + ".v", "w")
        f.write(netlist.generate())
