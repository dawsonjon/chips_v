clocks_per_sec = 50000000  # Clock speed in Hz
march = "rv32im"  # Architecture supported architectures are rv32im and rv32i
memory_size = 8 * 1024  # 8k bytes total memory
heap_size = 1  # proportion of memory reserved for heap (1 is minimum)
inputs = {"stdin": "stream"}  # List of inputs
outputs = {"stdout": "stream", "leds": ("uart", 50000000, 115200)}  # List of outputs
