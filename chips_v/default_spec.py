"""A default specification for the RISC-V SoC"""

default_settings = {
    "march": "rv32im",  # Select architecture supports rv32i or rv32im
    "memory_size": 1024 * 8,  # Shared instruction/data memory size in bytes
    "heap_size": 1024,  # Space in memory reserved for heap (malloc etc.) bytes
    "clocks_per_sec": 50000000,  # Clock Speed Hz
    "inputs": {"stdin": "stream"},  # Input streaming interface
    "outputs": {"stdout": "stream"},  # Output streaming interface
}
