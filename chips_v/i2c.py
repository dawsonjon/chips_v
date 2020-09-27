from baremetal import *
from baremetal.synchronous_process import *
from baremetal.unsigned import number_of_bits_needed

# -- COMMAND
# -- =======
# --
# -- Bits (7:0)
# -- ----------
# -- (For write byte only) data payload byte
# --
# -- Bit (8)
# -- -------
# -- 1 = read byte
# -- 0 = write byte
# --
# -- Bit (9)
# -- -------
# -- 1 = SEND_START
# --
# -- Bit (10)
# -- --------
# -- 1 = SEND_STOP
# --
# -- Bit (11)
# -- --------
# -- (For read byte only) 1 = SEND_ACK
# --
# -- RESPONSE
# -- ========
# --
# -- Bits (7:0)
# -- ----------
# -- (For read byte only) data payload byte
# --
# -- Bit (0)
# -- -------
# -- (For write byte only) 1 = NACK, 0 = ACK
# --


def i2c(clk, i2c_in, i2c_in_stb, i2c_out_ack, scl_i, sda_i, clocks_per_second, speed):

    i2c_delay = clocks_per_second / (2 * speed)

    sda_i = Boolean().register(clk, d=sda_i, init=0)
    sda_i = Boolean().register(clk, d=sda_i, init=0)
    sda_i = Boolean().register(clk, d=sda_i, init=0)
    scl_i = Boolean().register(clk, d=scl_i, init=0)
    scl_i = Boolean().register(clk, d=scl_i, init=0)
    scl_i = Boolean().register(clk, d=scl_i, init=0)

    (
        main_0,
        main_1,
        main_2,
        main_3,
        get_byte_0,
        get_byte_1,
        get_byte_2,
        get_byte_3,
        send_byte_0,
        send_byte_1,
        send_byte_2,
        send_byte_3,
        send_byte_4,
        send_bit_0,
        send_bit_1,
        send_bit_2,
        get_bit_0,
        get_bit_1,
        get_bit_2,
        send_start_0,
        send_start_1,
        send_start_2,
        send_start_3,
        send_start_4,
        send_stop_0,
        send_stop_1,
        send_stop_2,
        send_stop_3,
    ) = range(28)

    state = Unsigned(5).register(clk, init=main_0)
    i2c_out = Unsigned(32).register(clk, init=0)
    i2c_out_stb = Boolean().register(clk, init=0)
    i2c_in_ack = Boolean().register(clk, init=0)
    sda_o = Boolean().register(clk, init=1)
    scl_o = Boolean().register(clk, init=1)

    # sub procedure return addresses
    get_byte_return = Unsigned(5).register(clk, init=0)
    send_byte_return = Unsigned(5).register(clk, init=0)
    send_bit_return = Unsigned(5).register(clk, init=0)
    get_bit_return = Unsigned(5).register(clk, init=0)
    send_stop_return = Unsigned(5).register(clk, init=0)
    send_start_return = Unsigned(5).register(clk, init=0)

    # Timers/counters
    timer = Unsigned(number_of_bits_needed(i2c_delay)).register(clk, init=0)
    count = Unsigned(8).register(clk, init=0)
    bit = Boolean().register(clk, init=0)

    # command/response
    byte = Unsigned(8).register(clk, init=0)
    read_write = Boolean().register(clk, init=0)
    send_start = Boolean().register(clk, init=0)
    send_stop = Boolean().register(clk, init=0)
    send_ack = Boolean().register(clk, init=0)
    response = Unsigned(32).register(clk, init=0)
    started = Boolean().register(clk, init=0)

    Process(
        Switch(
            state,
            # main subroutine
            Case(
                main_0,
                Set(count, 7),
                Set(timer, i2c_delay),
                Set(state, main_1),
                Set(started, 0),
            ),
            Case(
                main_1,
                Set(i2c_in_ack, 1),
                If(
                    i2c_in_stb & i2c_in_ack,
                    Set(i2c_in_ack, 0),
                    Set(byte, i2c_in[7:0]),
                    Set(read_write, i2c_in[8]),
                    Set(send_start, i2c_in[9]),
                    Set(send_stop, i2c_in[10]),
                    Set(send_ack, i2c_in[11]),
                    Set(state, main_2),
                ),
            ),
            Case(
                main_2,
                If(
                    read_write,
                    Set(response, 0),
                    Set(state, get_byte_0),
                    Set(get_byte_return, main_3),
                ).Else(
                    Set(response, 0),
                    Set(state, send_byte_0),
                    Set(send_byte_return, main_3),
                ),
            ),
            Case(
                main_3,
                Set(i2c_out_stb, 1),
                Set(i2c_out, response),
                If(i2c_out_ack & i2c_out_stb, Set(i2c_out_stb, 0), Set(state, main_1),),
            ),
            # get byte subroutine
            Case(get_byte_0, Set(state, get_bit_0), Set(get_bit_return, get_byte_1),),
            Case(
                get_byte_1,
                Set(response, (response << 1) | bit),
                If(count == 0, Set(count, 7), Set(state, get_byte_2),).Else(
                    Set(count, count - 1), Set(state, get_byte_0),
                ),
            ),
            Case(
                get_byte_2,
                # send nack ack = 0 nack = 1
                Set(bit, send_ack),
                Set(state, send_bit_0),
                Set(send_bit_return, get_byte_3),
            ),
            Case(
                get_byte_3,
                If(
                    send_stop,
                    Set(state, send_stop_0),
                    Set(send_stop_return, get_byte_return),
                ).Else(Set(state, get_byte_return),),
            ),
            # send byte subroutine
            Case(
                send_byte_0,
                If(
                    send_start,
                    Set(state, send_start_0),
                    Set(send_start_return, send_byte_1),
                ).Else(Set(state, send_byte_1),),
            ),
            Case(
                send_byte_1,
                Set(bit, byte[7]),
                Set(byte, byte << 1),
                Set(state, send_bit_0),
                Set(send_bit_return, send_byte_2),
            ),
            Case(
                send_byte_2,
                If(count == 0, Set(count, 7), Set(state, send_byte_3),).Else(
                    Set(count, count - 1), Set(state, send_byte_1),
                ),
            ),
            Case(
                send_byte_3,
                # get ack
                Set(state, get_bit_0),
                Set(get_bit_return, send_byte_4),
            ),
            Case(
                send_byte_4,
                # 1 = nack, 0 = ack
                Set(response[0], bit),
                If(
                    send_stop,
                    Set(state, send_stop_0),
                    Set(send_stop_return, send_byte_return),
                ).Else(Set(state, send_byte_return),),
            ),
            # send start subroutine
            Case(
                send_start_0,
                If(started, Set(state, send_start_1),).Else(Set(state, send_start_4),),
            ),
            Case(
                send_start_1,
                Set(sda_o, 1),
                If(timer == 0, Set(timer, i2c_delay), Set(state, send_start_2),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(send_start_2, Set(scl_o, 1), If(scl_i, Set(state, send_start_3),),),
            Case(
                send_start_3,
                If(timer == 0, Set(timer, i2c_delay), Set(state, send_start_4),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(
                send_start_4,
                Set(sda_o, 0),
                If(
                    timer == 0,
                    Set(timer, i2c_delay),
                    Set(state, send_start_return),
                    Set(scl_o, 0),
                    Set(started, 1),
                ).Else(Set(timer, timer - 1),),
            ),
            # send stop subroutine
            Case(
                send_stop_0,
                Set(sda_o, 0),
                If(timer == 0, Set(timer, i2c_delay), Set(state, send_stop_1),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(send_stop_1, Set(scl_o, 1), If(scl_i, Set(state, send_stop_2))),
            Case(
                send_stop_2,
                If(
                    timer == 0,
                    Set(timer, i2c_delay),
                    Set(state, send_stop_3),
                    Set(sda_o, 1),
                ).Else(Set(timer, timer - 1),),
            ),
            Case(
                send_stop_3,
                If(
                    timer == 0,
                    Set(timer, i2c_delay),
                    Set(state, send_stop_return),
                    Set(started, 0),
                ).Else(Set(timer, timer - 1),),
            ),
            # send bit subroutine
            Case(
                send_bit_0,
                Set(sda_o, bit),
                If(timer == 0, Set(timer, i2c_delay), Set(state, send_bit_1),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(
                send_bit_1,
                Set(scl_o, 1),
                If(timer == 0, Set(timer, i2c_delay), Set(state, send_bit_2),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(
                send_bit_2,
                # clock stretching
                If(scl_i, Set(state, send_bit_return), Set(scl_o, 0),),
            ),
            # get bit subroutine
            Case(
                get_bit_0,
                Set(sda_o, 1),
                If(timer == 0, Set(timer, i2c_delay), Set(state, get_bit_1),).Else(
                    Set(timer, timer - 1),
                ),
            ),
            Case(
                get_bit_1,
                # clock stretching
                Set(scl_o, 1),
                If(scl_i, Set(state, get_bit_2),),
            ),
            Case(
                get_bit_2,
                If(
                    timer == 0,
                    Set(timer, i2c_delay),
                    Set(state, get_bit_return),
                    Set(bit, sda_i),
                    Set(scl_o, 0),
                ).Else(Set(timer, timer - 1),),
            ),
        )
    )

    return i2c_out, i2c_out_stb, i2c_in_ack, scl_o, sda_o


clk = Clock("clk")
i2c_in = Unsigned(32).input("i2c_in")
i2c_in_stb = Boolean().input("i2c_in_stb")
i2c_out_ack = Boolean().input("i2c_out_ack")
scl_i = Boolean().input("i2c_out_ack")
sda_i = Boolean().input("i2c_out_ack")

i2c_out, i2c_out_stb, i2c_in_ack, scl_o, sda_o = i2c(
    clk, i2c_in, i2c_in_stb, i2c_out_ack, scl_i, sda_i, 50000000, 5000000
)
