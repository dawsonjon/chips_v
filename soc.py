from baremetal import *

from assemble import *
from bus import Bus
from cpu import cpu
from debug_slave import debug_slave
from memory import create_soc_memory
from timer import timer
from output_stream import output_stream


def soc(clk, memory_size_words, memory_initial_contents):

    debug = Debug()
    output_streams = {}

    # create a bus
    bus = Bus()

    # connect slaves to bus
    pc = Unsigned(32).wire()
    pc_en = Boolean().wire()
    instruction = create_soc_memory(clk, memory_initial_contents,
                                    memory_size_words, pc, pc_en, bus)

    # debug slave
    output_streams["debug"] = output_stream(clk, bus, 0x12345678)

    # timer
    timer(clk, bus, 0x80000000)

    # create the CPU
    pc_, pc_en_, cpu_debug = cpu(instruction, clk, bus)
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

    return cpu_debug, debug, output_streams
