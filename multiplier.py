from baremetal import *

from utils import *


def multiplier(clk, a_in, b_in, a_signed, b_signed, go):

    debug = Debug()

    width = a_in.subtype.bits
    hwidth = width // 2
    dwidth = width * 2
    count, _ = counter(clk, 0, 4, 1, en=go)

    # stage 0
    a_in, b_in = register(clk, (count == 0), a_in, b_in)

    # stage 1
    a_negative = unsigned(a_in[width - 1])
    b_negative = unsigned(b_in[width - 1])
    a, b, z_negative = register(
        clk,
        (count == 1),
        unsigned(a_in.subtype.select(a_negative & a_signed, a_in, -a_in)),
        unsigned(b_in.subtype.select(b_negative & b_signed, b_in, -b_in)),
        (a_negative & a_signed) ^ (b_negative & b_signed)
    )

    # stage 2
    (
        product_a,
        product_b,
        product_c,
        product_d,
        z_negative
    ) = register(
        clk,
        (count == 2),
        a[hwidth - 1:0].resize(width) * b[hwidth - 1:0],
        a[hwidth - 1:0].resize(width) * b[width - 1:hwidth],
        a[width - 1:hwidth].resize(width) * b[hwidth - 1:0],
        a[width - 1:hwidth].resize(width) * b[width - 1:hwidth],
        z_negative
    )

    # stage 2
    (
        product,
        z_negative,
    ) = register(
        clk,
        (count == 3),
        (
            product_a.resize(dwidth) +
            (product_b.resize(dwidth) << hwidth) +
            (product_c.resize(dwidth) << hwidth) +
            (product_d.resize(dwidth) << width)
        ),
        z_negative,
    )
    debug.product = product
    debug.product_a = product_a
    debug.product_b = product_b
    debug.product_c = product_c
    debug.product_d = product_d
    debug.a = a
    debug.b = b
    product = z_negative.subtype.select(z_negative, product, -product)

    return product[dwidth - 1:width], product[width - 1:0], (count == 4), debug


def test_multiply(clk, a, b, z, y, go, done, debug, a_val, b_val):
    a.set(a_val)
    b.set(b_val)
    go.set(1)
    while 1:
        debug.display()
        done_v = done.get()
        z_v = z.get()
        y_v = y.get()
        clk.tick()
        if done_v:
            go.set(0)
            return z_v, y_v


if __name__ == "__main__":

    clk = Clock("clk")
    a = Unsigned(4).input("a")
    b = Unsigned(4).input("b")
    signed_a = Boolean().input("signed_a")
    signed_b = Boolean().input("signed_b")
    go = Boolean().input("go")

    z, y, done, debug = multiplier(clk, a, b, signed_a, signed_b, go)
    clk.initialise()

    # Test in unsigned configuration
    def hi(x):
        return x >> 4 & 0xf

    def lo(x):
        return x & 0xf

    signed_a.set(0)
    signed_b.set(0)
    for a_val in range(16):
        for b_val in range(16):
            h, l = test_multiply(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            print(a_val, b_val, h & 0xf, l & 0xf, hi(
                a_val * b_val), lo(a_val * b_val))
            assert h & 0xf == hi(a_val * b_val)
            assert l & 0xf == lo(a_val * b_val)

    signed_a.set(1)
    signed_b.set(0)
    for a_val in range(-8, 8):
        for b_val in range(16):
            h, l = test_multiply(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            print(a_val, b_val, h & 0xf, l & 0xf, hi(
                a_val * b_val), lo(a_val * b_val))
            assert h & 0xf == hi(a_val * b_val)
            assert l & 0xf == lo(a_val * b_val)

    signed_a.set(1)
    signed_b.set(1)
    for a_val in range(-8, 8):
        for b_val in range(-8, 8):
            h, l = test_multiply(
                clk, a, b, z, y, go, done, debug, a_val, b_val)
            print(a_val, b_val, h & 0xf, l & 0xf, hi(
                a_val * b_val), lo(a_val * b_val))
            assert h & 0xf == hi(a_val * b_val)
            assert l & 0xf == lo(a_val * b_val)
