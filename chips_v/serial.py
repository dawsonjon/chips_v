from baremetal import *
from baremetal.synchronous_process import *
from baremetal.unsigned import number_of_bits_needed
from chips_v.utils import Debug
from chips_v.utils import shex


def serial_in(clk, rx, rx_ready, clk_rate, baud_rate):

    rx = Boolean().register(clk, d=rx, init=1)
    rx = Boolean().register(clk, d=rx, init=1)
    rx = Boolean().register(clk, d=rx, init=1)

    baud_divide = round(clk_rate / baud_rate) - 1
    baud_divide_1x5 = round((clk_rate * 1.5) / baud_rate) - 1

    idle = 0
    get = 1
    stop = 2
    send = 4

    state = Unsigned(3).register(clk, init=idle)
    bit = Unsigned(3).register(clk, init=0)
    rx_data = Unsigned(8).register(clk, init=0)
    rx_valid = Boolean().register(clk, init=0)
    counter = Unsigned(number_of_bits_needed(baud_divide_1x5)).register(clk, init=0)

    Process(
        Switch(
            state,
            Case(
                idle,
                If(~rx, Set(state, get), Set(counter, baud_divide_1x5), Set(bit, 0),),
            ),
            Case(
                get,
                If(
                    counter == 0,
                    Set(rx_data, cat(rx, rx_data[7:1])),
                    Set(counter, baud_divide),
                    If(bit == 7, Set(counter, baud_divide), Set(state, stop),).Else(
                        Set(bit, bit + 1)
                    ),
                ).Else(Set(counter, counter - 1)),
            ),
            Case(stop, If(rx, Set(state, send), Set(rx_valid, 1),)),
            Case(send, If(rx_ready, Set(state, idle), Set(rx_valid, 0),)),
        )
    )

    debug = Debug()
    debug.count = counter
    debug.bit = bit
    debug.rx = rx
    debug.rx_data = rx_data
    debug.rx_valid = rx_valid
    debug.rx_ready = rx_ready

    return rx_valid, rx_data, debug


def serial_out(clk, tx_data, tx_valid, clk_rate, baud_rate):

    baud_divide = round(clk_rate / baud_rate) - 1

    idle = 0
    start = 1
    send = 2
    stop = 4

    state = Unsigned(3).register(clk, init=idle)
    bit = Unsigned(3).register(clk, init=0)
    shift_reg = Unsigned(8).register(clk, init=0)
    tx_ready = Boolean().register(clk, init=1)
    tx = Boolean().register(clk, init=1)
    counter = Unsigned(number_of_bits_needed(baud_divide)).register(clk, init=0)

    Process(
        Switch(
            state,
            Case(
                idle,
                If(
                    tx_valid,
                    Set(shift_reg, tx_data),
                    Set(state, start),
                    Set(counter, baud_divide),
                    Set(tx_ready, 0),
                    Set(tx, 0),
                ),
            ),
            Case(
                start,
                If(
                    counter == 0,
                    Set(state, send),
                    Set(counter, baud_divide),
                    Set(bit, 0),
                    Set(tx, shift_reg[0]),
                    Set(shift_reg, shift_reg >> 1),
                ).Else(Set(counter, counter - 1),),
            ),
            Case(
                send,
                If(
                    counter == 0,
                    Set(shift_reg, shift_reg >> 1),
                    Set(tx, shift_reg[0]),
                    Set(counter, baud_divide),
                    If(bit == 7, Set(tx, 1), Set(state, stop),).Else(Set(bit, bit + 1)),
                ).Else(Set(counter, counter - 1),),
            ),
            Case(
                stop,
                If(counter == 0, Set(state, idle), Set(tx_ready, 1),).Else(
                    Set(counter, counter - 1),
                ),
            ),
        )
    )

    debug = Debug()
    debug.state = state
    debug.tx_valid = tx_valid
    debug.tx_ready = tx_ready
    debug.tx_data = tx_data
    debug.tx = tx

    return tx_ready, tx, debug


def test():
    print("testing serial")

    clk = Clock("clk")

    tx_data = Unsigned(8).input("tx_data")
    valid = Boolean().input("valid")
    ready, tx, debug = serial_out(clk, tx_data, valid, 100, 10)

    rx_ready = Boolean().input("ready")
    rx_valid, rx_data, rx_debug = serial_in(clk, tx, rx_ready, 100, 10)

    clk.initialise()

    stimulus = iter([0xAA, 0x55, 0xFF, 0x00, 0xAA, 0x55, 0xFF, 0x00])
    response = iter([0xAA, 0x55, 0xFF, 0x00, 0xAA, 0x55, 0xFF, 0x00])
    tx_data.set(next(stimulus))
    rx_ready.set(1)
    valid.set(1)
    for i in range(1000):

        try:
            if rx_valid.get():
                # print(shex(rx_data.get()))
                if rx_data.get() != next(response):
                    # print("fail")
                    return False
            next_data = ready.get()
            # debug.display()
            clk.tick()
            if next_data:
                value = next(stimulus)
                tx_data.set(value)
        except StopIteration:
            return True
