import os

import chips_v.input_stream
import chips_v.output_stream
from baremetal import *
from chips_v.assemble import *
from chips_v.bus import Bus
from chips_v.cpu import cpu
from chips_v.default_spec import default_settings
from chips_v.memory import create_soc_memory
from chips_v.timer import timer


class Soc:

    def __init__(self, clk, memory_size_words, memory_initial_contents,
                 settings=default_settings):

        self.clk = clk

        debug = Debug()
        output_streams = {}
        input_streams = {}

        # create a bus
        bus = Bus()

        # connect slaves to bus
        pc = Unsigned(32).wire()
        pc_en = Boolean().wire()
        instruction = create_soc_memory(clk, memory_initial_contents,
                                        memory_size_words, pc, pc_en, bus)

        # timer
        timer(clk, bus, 0x80000000)

        # output_streams
        next_address = 0x80000008
        for outp in settings["outputs"]:
            output_streams[outp] = chips_v.output_stream.output_stream(
                clk, bus, next_address)
            next_address += 4
        for inp in settings["inputs"]:
            input_streams[inp] = chips_v.input_stream.input_stream(
                clk, bus, next_address)
            next_address += 4

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
        self.output_streams = output_streams
        self.input_streams = input_streams

    def simulate(self, cycles, print_debug=False, verbose=False,
                 print_memory=False):

        cpu_debug = self.cpu_debug
        soc_debug = self.soc_debug
        output_streams = self.output_streams
        input_streams = self.input_streams

        # acknowledge all output streams
        for name, output_stream in output_streams.items():
            inp = Boolean().input(name)
            output_stream.ready.drive(inp)
            inp.set(1)

        # provide null response to input streams
        for name, input_stream in input_streams.items():
            inp = Boolean().input(name + "_valid")
            input_stream.valid.drive(inp)
            inp.set(1)
            inp = input_stream.data.subtype.input(name)
            input_stream.data.drive(inp)
            inp.set(0)

        self.clk.initialise()
        elapsed = 0
        while 1:

            if verbose:
                if cpu_debug.global_enable.get():
                    if cpu_debug.execute_en.get():
                        print(">... ", hex(cpu_debug.this_pc.get()), end=' ')
                        print_instruction(cpu_debug.instruction.get())

                    else:
                        print("X... filling")
                else:
                    print("X... waiting for data", print_instruction(
                        cpu_debug.instruction.get()))

            # debug text
            if print_debug:
                cpu_debug.display()
                soc_debug.display()

            if print_memory:
                # memory access
                if (soc_debug.data_valid.get() &
                    soc_debug.data_ready.get() &
                        ~soc_debug.write_read.get()):
                    print("        reading: memory[%s]" %
                          (shex(soc_debug.address.get())))
                    print("             got: [%s]" %
                          (shex(soc_debug.data_in.get())))

                if (soc_debug.data_valid.get() &
                    soc_debug.data_ready.get() &
                        soc_debug.write_read.get()):
                    print("        writing: memory[%s]" % (
                        shex(soc_debug.address.get())),
                        "byte:", sbin(soc_debug.byte_enable.get()))
                    print("             with: [%s]" %
                          (shex(soc_debug.data_out.get())))

            for name, output_stream in output_streams.items():
                if output_stream.valid.get():
                    print(name)
                    print("    output: %s: %s %x" % (
                        name,
                        chr(output_stream.data.get()),
                        output_stream.data.get())
                    )
                # use special values to pass or fail compliance test
                if name == "stdout" and output_stream.data.get() == 0x600d:
                    return True
                if name == "stdout" and output_stream.data.get() == 0xbad:
                    return False

            # stop simulation if infinite loop encountered
            if cpu_debug.global_enable.get():
                if cpu_debug.execute_en.get():
                    if cpu_debug.take_branch.get():
                        if (cpu_debug.this_pc.get() ==
                                cpu_debug.branch_address.get()):
                            print("cpu halted")
                            return True

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
        for name, output_stream in self.output_streams.items():
            inp = Boolean().input(name + "_ready_in")
            output_stream.ready.drive(inp)
            inputs.append(inp)
            outp = Boolean().output(name + "_valid_out", output_stream.valid)
            outputs.append(outp)
            subtype = output_stream.data.subtype
            outp = subtype.output(name + "_out", output_stream.data)
            outputs.append(outp)

        # Populate a list of inputs and outputs
        for name, input_stream in self.input_streams.items():
            inp = Boolean().input(name + "_valid_in")
            input_stream.valid.drive(inp)
            inputs.append(inp)

            subtype = input_stream.data.subtype
            inp = subtype.input(name + "_data_in")
            input_stream.data.drive(inp)
            inputs.append(inp)
            outp = Boolean().output(name + "_ready_out", input_stream.ready)
            outputs.append(outp)

        # Generate verilog netlist
        netlist = Netlist(
            netlist_name,
            [self.clk],
            inputs,
            outputs
        )
        f = open(netlist_name + ".v", "w")
        f.write(netlist.generate())
