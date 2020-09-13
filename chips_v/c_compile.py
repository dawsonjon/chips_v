import os
import subprocess
import sys


def read_binfile(binfile):
    with open(binfile, "rb") as f:
        bindata = f.read()
    
    instructions = []
    for i in range(len(bindata) // 4):
        w = bindata[4 * i: 4 * i + 4]
        instructions.append(w[3] << 24 | w[2] << 16 | w[1] << 8 | w[0])

    return instructions

def c_compile(input_files):
    directory = os.path.abspath(__file__)
    directory = os.path.dirname(directory)
    include = os.path.join(directory, "include")
    link_script = os.path.join(directory, "ld", "link.ld")
    startup = os.path.join(directory, "ld", "start.S")

    #Compile into an elf file
    compile_command=("/opt/riscv/bin/riscv32-unknown-elf-gcc -Os -I %s " 
                     "-march=rv32im -mcmodel=medlow -ffunction-sections "
                     "-Wl,--gc-sections "
                     "-fdata-sections --specs=nosys.specs -nostartfiles "
                     "-T %s -o main.elf %s %s")

    compile_command=compile_command%(
        include, 
        link_script, 
        startup,
        " ".join(input_files), 
    )

    result = subprocess.call(compile_command, shell=True)
    if result != 0:
        sys.exit(1)

    #convert to binary file
    copy_command=("/opt/riscv/bin/riscv32-unknown-elf-objcopy -S -O binary"
                  " main.elf main.bin")
    result = subprocess.call(copy_command, shell=True)
    if result != 0:
        sys.exit(1)

    #convert to a list of instructions
    instructions=read_binfile("main.bin")

    return instructions
