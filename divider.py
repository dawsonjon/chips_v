from baremetal import *

from utils import *


def divider(clk, a_in, b_in, signedd, go):

    debug = Debug()

    width = a_in.subtype.bits
    t_data = unsigned(a_in).subtype

    count, _ = counter(clk, 0, width + 5, 1, en=go)
    reset_registers = (count == 2)
    register_outputs = (width + 3 == count)
    negate_outputs = (width + 4 == count)
    done = (width + 5 == count)
    debug.count = count

    # Stage 0 register inputs
    a_in, b_in = register(
        clk,
        count == 0,
        a_in, b_in
    )
    a_signed = a_in

    # Stage 1 calculate signs
    a_negative = unsigned(a_in[width - 1])
    b_negative = unsigned(b_in[width - 1])
    a_in, b_in, a_negative, z_negative = register(
        clk,
        count == 1,
        unsigned(a_in.subtype.select(a_negative & signedd, a_in, -a_in)),
        unsigned(b_in.subtype.select(b_negative & signedd, b_in, -b_in)),
        a_negative,
        a_negative ^ b_negative
    )

    # Stage 3 .. width + 3
    remainder = t_data.register(clk, init=0)
    z = t_data.register(clk, init=0)
    a = t_data.register(clk, init=0)

    shifter = cat(remainder[width - 1:0], a[width - 1])
    difference = shifter.resize(width + 1) - b_in
    shifter_gt_b = ~difference[width]

    next_remainder = t_data.select(shifter_gt_b, shifter, difference)
    next_z = t_data.select(shifter_gt_b, z << 1, (z << 1) | 1)
    next_a = a << 1

    next_remainder = t_data.select(reset_registers, next_remainder, 0)
    next_gain = t_data.select(reset_registers, next_z, 0)
    next_a = t_data.select(reset_registers, next_a, a_in)

    remainder.d(next_remainder)
    z.d(next_gain)
    a.d(next_a)
    z = t_data.register(clk, init=0, en=register_outputs, d=z)
    y = t_data.register(clk, init=0, en=register_outputs, d=remainder)

    # Stage width + 4 negate outputs
    z = signed(z.subtype.select(z_negative & signedd, z, -z))
    y = signed(y.subtype.select(a_negative & signedd, y, -y))
    z, y = register(
        clk,
        negate_outputs,
        z.subtype.select((b_in == 0) & signedd, z, - 1),
        y.subtype.select((b_in == 0) & signedd, y, a_signed),
    )

    return z, y, done, debug


def test_divide(clk, a, b, z, y, go, done, debug, a_val, b_val):
    a.set(a_val)
    b.set(b_val)
    go.set(1)
    while 1:
        # debug.display()
        done_v = done.get()
        result_v = z.get()
        mod_v = y.get()
        clk.tick()
        if done_v:
            go.set(0)
            return result_v, mod_v


def divide_model(a, b, bits):

    # handle divide by zero according to riscv spec
    if b == 0:
        return (2 ** bits) - 1

    z = a // b

    return z


def modulo_model(a, b):

    # handle divide by zero according to riscv spec
    if b == 0:
        return a

    z = a % b

    return z


def signed_divide(a, b, bits):

    # handle divide by zero according to riscv spec
    if b == 0:
        return -1

    # overflow according to riscv spec
    if a == -(2 ** (bits - 1)) and b == -1:
        return -(2 ** (bits - 1))

    a_signed = a < 0
    b_signed = b < 0
    z_signed = a_signed ^ b_signed
    z = abs(a) // abs(b)
    if z_signed:
        return -z
    return z


def signed_mod(a, b):

    # handle divide by zero according to riscv spec
    if b == 0:
        return a

    a_signed = a < 0
    z = abs(a) % abs(b)
    if a_signed:
        return -z
    return z


if __name__ == "__main__":

    clk = Clock("clk")
    a = Signed(4).input("a")
    b = Signed(4).input("b")
    go = Boolean().input("go")
    signedd = Boolean().input("signedd")

    z, y, done, debug = divider(clk, a, b, signedd, go)
    clk.initialise()

    signedd.set(1)
    for a_val in range(-8, 8):
        for b_val in range(-8, 8):
            result, mod = test_divide(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            assert result == signed_divide(a_val, b_val, 4)
            assert mod == signed_mod(a_val, b_val)
    print("divider test1 ... pass")

    signedd.set(0)
    for a_val in range(16):
        for b_val in range(16):
            result, mod = test_divide(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            result &= 0xf
            mod &= 0xf
            assert result == divide_model(a_val, b_val, 4)
            assert mod == modulo_model(a_val, b_val)
    print("divider test2 ... pass")
