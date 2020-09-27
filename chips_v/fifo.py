"""FIFO"""

from baremetal import *


def fifo(clk, data_in, data_in_stb, data_out_ack, depth):

    read = Boolean().wire()
    write = Boolean().wire()

    input_counter, _ = counter(0, depth - 1, 1, read)
    output_counter, _ = counter(0, depth - 1, 1, write)

    memory = data_in.subtype.RAM(clk, depth, synchronous=True)
    memory.write(data_in, input_counter, write)
    data_out = memory.read(output_counter, read)

    full = input_counter == output_counter - 1
    empty = input_counter == output_counter

    data_in_ack = not full
    data_out_stb = Boolean().register(
        clk, d=read | (data_out_stb & ~data_out_ack), init=0
    )

    write.drive(data_in_ack & data_in_stb)
    read.drive(~empty & (~data_out_stb | data_out_ack))

    return data_out, data_out_stb, data_in_ack
