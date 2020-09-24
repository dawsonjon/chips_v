"""A programmable PWM output"""
from baremetal import *


def pwm(clk, data, data_valid, clock_frequency, output_frequency, bits):

    # Generate sawtooth wave for comparison
    prescale = clock_frequency / (output_frequency * (2 ** bits))
    _, last = counter(clk, 0, prescale - 1, 1, en=1)
    sawtooth, _ = counter(clk, 0, (2 ** bits) - 1, 1, en=last)

    # register new data values
    value = data[bits:0]
    value = value.subtype.register(clk, d=data, init=0, en=data_valid)

    # Generate PWM
    pwm = value > sawtooth

    return pwm
