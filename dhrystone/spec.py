from chips_v.peripherals import *

clocks_per_sec = 50000000
march = "rv32im"
memory_size = 64 * 1024
heap_size = 16 * 1024
peripherals = [OutputStream("stdout"), InputStream("stdin")]
