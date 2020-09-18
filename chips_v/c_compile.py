"""Provide an interface with the RISC-V GNU Toolchain."""


import os
import shutil
import subprocess

from chips_v.default_spec import default_settings


class CompileError(Exception):
    pass


class BinaryError(Exception):
    pass


def generate_linker_script(settings):

    link_ld = """OUTPUT_ARCH( "riscv" )
    ENTRY( _start )

    MEMORY
    {
      RAM   (rwx) : ORIGIN = 0x00000000, LENGTH = MEM_SIZE
    }

    SECTIONS
    {
      .text : {
            . = 0x000000;
            *(.init);
            *(.text);
            . = ALIGN(4);
            *(.data);
            *(.rodata);
            *(.srodata);
            *(.bss);
            *(.sdata);
            _end = .;
      } >RAM
    }""".replace(
        "MEM_SIZE", str(settings["memory_size"])
    )

    link_ld_file = os.path.join("__chips__", "link.ld")
    with open(link_ld_file, "w") as f:
        f.write("".join(link_ld))


def generate_header(settings):

    header = ["//Auto Generated Machine Description Header\n"]
    header = ["extern const unsigned int CLOCKS_PER_SEC;\n"]

    # Add memory locations of outputs
    for output in settings["outputs"]:
        header.append("extern const unsigned int %s;\n" % output)

    # Add memory locations of inputs
    for inp in settings["inputs"]:
        header.append("extern const unsigned int %s;\n" % inp)

    header = """
#ifndef __MACHINE_H__
#define __MACHINE_H__
%s
#endif
    """ % "".join(
        header
    )

    machine_h = os.path.join("__chips__", "include", "machine.h")
    with open(machine_h, "w") as f:
        f.write(header)


def generate_machine_spec(settings):

    address = 0x80000008
    source = ["//Auto Generated Machine Description Header\n"]
    source.append(
        "const unsigned int CLOCKS_PER_SEC = %u;\n" % settings["clocks_per_sec"]
    )
    heap_size_words = (settings["heap_size"] + 3) // 4
    source.append("//The heap is implemented as a global array\n")
    source.append("const int heap_size = %u;\n" % heap_size_words)
    source.append("int heap[%u] = {0};\n" % heap_size_words)

    # Add memory locations of outputs
    for output in settings["outputs"]:
        source.append("const unsigned int %s = 0x%xu;\n" % (output, address))
        address += 4

    # Add memory locations of inputs
    for inp in settings["inputs"]:
        source.append("const unsigned int %s = 0x%xu;\n" % (inp, address))
        address += 4

    source = "".join(source)

    machine_c = os.path.join("__chips__", "machine.c")
    with open(machine_c, "w") as f:
        f.write(source)


def generate_start_code(settings):
    start_s = """
.section .init
.global main
.global _start

_start:
    li x1, 0;
    li x2, 0;
    li x3, 0;
    li x4, 0;
    li x5, 0;
    li x6, 0;
    li x7, 0;
    li x8, 0;
    li x9, 0;
    li x10, 0;
    li x11, 0;
    li x12, 0;
    li x13, 0;
    li x14, 0;
    li x15, 0;
    li x16, 0;
    li x17, 0;
    li x18, 0;
    li x19, 0;
    li x20, 0;
    li x21, 0;
    li x22, 0;
    li x23, 0;
    li x24, 0;
    li x25, 0;
    li x26, 0;
    li x27, 0;
    li x28, 0;
    li x29, 0;
    li x30, 0;
    li x31, 0;
    /* set stack pointer */
    lui sp, %hi(MEM_SIZE)
    addi sp, sp, %lo(MEM_SIZE)

    /* call main */
    jal ra, main

    /* break */
_end:
    j _end""".replace(
        "MEM_SIZE", str(settings["memory_size"] - 4)
    )

    machine_h = os.path.join("__chips__", "start.S")
    with open(machine_h, "w") as f:
        f.write("".join(start_s))


def read_binfile(binfile):
    with open(binfile, "rb") as f:
        bindata = f.read()

    # pad to a multiple of 4 bytes
    pad_bytes = 4 - (len(bindata) % 4)
    for i in range(pad_bytes):
        bindata += b"\x00"

    instructions = []
    for i in range(len(bindata) // 4):
        w = bindata[4 * i : 4 * i + 4]
        instructions.append(w[3] << 24 | w[2] << 16 | w[1] << 8 | w[0])

    return instructions


def c_compile(input_files, settings=default_settings, compile_flags=""):

    # Create a working folder to perform the build
    if os.path.exists("__chips__"):
        shutil.rmtree("__chips__")
    os.mkdir("__chips__")
    os.mkdir(os.path.join("__chips__", "include"))

    # generate machine specific header
    generate_header(settings)

    # generate machine specific header
    generate_machine_spec(settings)

    # generate machine specific startup code
    generate_start_code(settings)

    # generate machine specific link script
    generate_linker_script(settings)

    # Create a static include directory
    directory = os.path.abspath(__file__)
    directory = os.path.dirname(directory)
    include = os.path.join(directory, "include")
    libspath = os.path.join(directory, "libs")
    local_include = " %s" % os.path.abspath(os.path.join("__chips__", "include"))
    input_files = [os.path.abspath(i) for i in input_files]
    link_script = "./link.ld"

    # use custom versions of some library components
    libc = os.path.join(libspath, "stdio.o") + " "
    libc += os.path.join(libspath, "printf.o") + " "
    libc += os.path.join(libspath, "malloc.o") + " "
    libc += os.path.join(libspath, "string.o") + " "
    libc += os.path.join(libspath, "ctype.o") + " "
    libc += os.path.join(libspath, "time.o") + " "

    # Compile into an elf file
    compile_command = (
        "/opt/riscv/bin/riscv32-unknown-elf-gcc -I%s -I%s "
        "-march=%s -mcmodel=medlow -ffunction-sections "
        "-Wno-builtin-declaration-mismatch "
        "-Wl,--gc-sections "
        "-fdata-sections -specs=nosys.specs -nostartfiles "
        "-specs=nano.specs "
        "%s "
        "-T %s -o main.elf start.S machine.c %s %s"
    )

    compile_command = compile_command % (
        local_include,
        include,
        settings["march"],
        compile_flags,
        link_script,
        libc,
        " ".join(input_files),
    )

    print(compile_command)

    # move into working directory
    starting_dir = os.getcwd()
    os.chdir("__chips__")

    try:

        # run compiler
        result = subprocess.call(compile_command, shell=True)
        if result != 0:
            raise CompileError

        # convert to binary file
        copy_command = (
            "/opt/riscv/bin/riscv32-unknown-elf-objcopy -S -O binary"
            " main.elf main.bin"
        )
        result = subprocess.call(copy_command, shell=True)
        if result != 0:
            raise BinaryError

        # convert to a list of instructions
        instructions = read_binfile("main.bin")

    finally:
        os.chdir(starting_dir)

    return instructions
