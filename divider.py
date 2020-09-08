from baremetal import *

from utils import *


def divider(clk, a_in, b_in, go):

    debug = Debug()

    width = a_in.subtype.bits
    t_data = a_in.subtype
    done = Boolean().wire()

    count, last = counter(clk, 0, width + 3, 1, en=go)
    register_inputs = (count == 0)
    reset_registers = (count == 1)
    register_outputs = (width + 2 == count)
    done = (width + 3 == count)

    a_in = t_data.register(clk, init=0, en=register_inputs, d=a_in)
    b_in = t_data.register(clk, init=0, en=register_inputs, d=b_in)

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

    debug.z = z
    z = t_data.register(clk, init=0, en=register_outputs, d=z)
    y = t_data.register(clk, init=0, en=register_outputs, d=remainder)

    debug.reset_registers = reset_registers
    debug.register_inputs = register_inputs
    debug.result = z
    debug.count = count
    debug.go = go
    debug.done = done
    debug.shifter = shifter
    debug.remainder = remainder
    debug.difference = difference
    debug.b_in = b_in
    debug.a = a

    return z, y, done, debug


def sdivider(clk, a_in, b_in, signedd, go):

    width = a_in.subtype.bits

    debug = Debug()
    debug.a_in = a_in
    debug.b_in = b_in

    a_negative = unsigned(a_in[width - 1])
    b_negative = unsigned(b_in[width - 1])
    a = a_in.subtype.select(a_negative & signedd, a_in, -a_in)
    b = b_in.subtype.select(b_negative & signedd, b_in, -b_in)
    z_negative = a_negative ^ b_negative

    debug.a_negative = a_negative
    debug.b_negative = b_negative
    debug.z_negative = z_negative
    debug.a = unsigned(a)
    debug.b = unsigned(b)

    z, y, done, _ = divider(clk, unsigned(a), unsigned(b), go)

    debug.z = unsigned(z)

    z = signed(z.subtype.select(z_negative & signedd, z, -z))
    y = signed(y.subtype.select(b_negative & signedd, y, -y))

    z = z.subtype.select((b == 0) & signedd, z, - 1)
    y = y.subtype.select((b == 0) & signedd, y, a_in)

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


def test_sdivide(clk, a, b, z, y, go, done, debug, a_val, b_val):
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


def divide(a, b, bits):

    # handle divide by zero according to riscv spec
    if b == 0:
        return (2 ** bits) - 1

    return z


def modulo(a, b):

    # handle divide by zero according to riscv spec
    if b == 0:
        return a
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

    b_signed = b < 0
    z = abs(a) % abs(b)
    if b_signed:
        return -z
    return z


if __name__ == "__main__":

    clk = Clock("clk")
    a = Unsigned(4).input("a")
    b = Unsigned(4).input("b")
    go = Boolean().input("go")

    z, y, done, debug = divider(clk, a, b, go)
    clk.initialise()

    for a_val in range(16):
        for b_val in range(16):
            result, mod = test_divide(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            assert result == divide(a_val, b_val, 4)
            assert mod == modulo(a_val, b_val)
    print("divider test1 ... pass")

    clk = Clock("clk")
    a = Signed(4).input("a")
    b = Signed(4).input("b")
    go = Boolean().input("go")
    signedd = Boolean().input("signedd")

    z, y, done, debug = sdivider(clk, a, b, signedd, go)
    clk.initialise()

    signedd.set(1)
    for a_val in range(-8, 8):
        for b_val in range(-8, 8):
            result, mod = test_sdivide(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            assert result == signed_divide(a_val, b_val, 4)
            assert mod == signed_mod(a_val, b_val)
    print("divider test2 ... pass")

    signedd.set(0)
    for a_val in range(16):
        for b_val in range(16):
            result, mod = test_sdivide(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            result &= 0xf
            mod &= 0xf
            assert result == divide(a_val, b_val, 4)
            assert mod == modulo(a_val, b_val)
    print("divider test3 ... pass")
