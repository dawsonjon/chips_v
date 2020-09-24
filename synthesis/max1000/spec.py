from chips_v.peripherals import *

clocks_per_sec = 50000000
march = "rv32im"
memory_size = 20 * 1024
heap_size = 1 * 1024
peripherals = [
    InputSerial("stdin", clocks_per_sec, 115200),
    OutputSerial("stdout", clocks_per_sec, 115200),
    OutputPin("leds"),
    OutputPWM("pwm", clocks_per_sec, 10000, 10),
]
