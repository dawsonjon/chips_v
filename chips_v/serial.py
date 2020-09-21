from baremetal import *
from chips_v.utils import Debug
from chips_v.utils import shex


def serial_in(clk, rx, rx_ready, clk_rate, baud_rate):

    rx = Boolean().register(clk, d=rx, init=1)
    rx = Boolean().register(clk, d=rx, init=1)
    rx = Boolean().register(clk, d=rx, init=1)

    baud_divide = round(clk_rate / baud_rate)
    baud_divide_1x5 = round((clk_rate * 1.5) / baud_rate)

    # Control state machine
    done = Boolean().wire()

    idle = Boolean().register(clk, init=1)
    idle.d(done | (idle & rx))

    start = Boolean().register(clk, init=0)
    start_count, last_start_count = counter(clk, 0, baud_divide_1x5 - 2, 1, en=start)
    start.d(idle & ~rx | start & ~(last_start_count))

    get = Boolean().register(clk, init=0)
    baud_count, last_baud_count = counter(clk, 0, baud_divide - 1, 1, en=get)
    bit_count, last_bit_count = counter(clk, 0, 7, 1, en=get & last_baud_count)
    get.d((start & last_start_count) | (get & ~(last_baud_count & last_bit_count)))

    send = Boolean().register(clk, init=0)
    send.d((get & last_baud_count & last_bit_count) | send & ~rx_ready)
    rx_valid = send

    done.drive(send & rx_ready)

    # Data register
    rx_data = Unsigned(8).register(clk, init=0, en=get & (baud_count == 0))
    rx_data.d(cat(rx, rx_data[7:1]))

    debug = Debug()
    debug.rx = rx

    debug.idle = idle
    debug.start = start
    debug.get = get
    debug.send = send
    debug.baud_count = baud_count
    debug.rx_data = rx_data
    debug.rx_valid = rx_valid
    debug.rx_ready = rx_ready

    return rx_valid, rx_data, debug


def serial_out(clk, tx_data, tx_valid, clk_rate, baud_rate):

    input_data = tx_data
    baud_divide = round(clk_rate / baud_rate)

    # Control state machine
    done = Boolean().wire()

    idle = Boolean().register(clk, init=1)
    idle.d(done | (idle & ~tx_valid))
    tx_ready = idle

    start = Boolean().register(clk, init=0)
    start_count, last_start_count = counter(clk, 0, baud_divide - 1, 1, en=start)
    start.d(idle & tx_valid | start & ~(last_start_count))

    send = Boolean().register(clk, init=0)
    baud_count, last_baud_count = counter(clk, 0, baud_divide - 1, 1, en=send)
    bit_count, last_bit_count = counter(clk, 0, 7, 1, en=send & last_baud_count)
    send.d((start & last_start_count) | (send & ~(last_baud_count & last_bit_count)))

    stop = Boolean().register(clk, init=0)
    stop_count, last_stop_count = counter(clk, 0, baud_divide - 1, 1, en=stop)
    stop.d((send & last_baud_count & last_bit_count) | stop & ~last_stop_count)
    done.drive(stop & last_stop_count)

    # Data register
    load_data = tx_data
    tx_data = Unsigned(8).register(clk, init=0)
    next_data = Unsigned(8).select(send & last_baud_count, tx_data, tx_data >> 1)
    next_data = Unsigned(8).select(idle & tx_valid, next_data, load_data)
    tx_data.d(next_data)
    tx = tx_data[0]
    tx = Boolean().select(start, tx, 0)
    tx = Boolean().select(idle | stop, tx, 1)

    debug = Debug()
    debug.input_data = input_data
    debug.idle = idle
    debug.tx_valid = tx_valid
    debug.start = start
    debug.start_count = start_count
    debug.last_start_count = last_start_count
    debug.send = send
    debug.baud_count = baud_count
    debug.bit_count = bit_count
    debug.last_bit_count = last_bit_count
    debug.stop = stop
    debug.stop_count = stop_count
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
                    return False
            next_data = ready.get()
            # debug.display()
            clk.tick()
            if next_data:
                value = next(stimulus)
                tx_data.set(value)
        except StopIteration:
            return True
