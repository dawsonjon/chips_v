clocks_per_sec = 50000000
march = "rv32im"
memory_size = 20 * 1024
heap_size = 1 * 1024
inputs = {"stdin": ("uart", 50000000, 115200)}
outputs = {"stdout": ("uart", 50000000, 115200), "leds": "pin"}
