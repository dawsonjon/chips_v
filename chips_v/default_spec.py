"""A default specification for the RISC-V SoC"""

from chips_v.peripherals import *

default_settings = {
    "march": "rv32im",  # Select architecture supports rv32i or rv32im
    "memory_size": 1024 * 8,  # Shared instruction/data memory size in bytes
    "heap_size": 1024,  # Space in memory reserved for heap (malloc etc.) bytes
    "clocks_per_sec": 50000000,  # Clock Speed Hz
    "peripherals": [
        InputStream("stdin"),
        OutputStream("stdout"),
    ],  # Input streaming interface
}
