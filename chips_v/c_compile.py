import os
import subprocess
import sys
import shutil

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
            *(.rodata);
            *(.sdata);
            *(.bss);
            _end = .;
      } >RAM
    }""".replace("MEM_SIZE", str(settings["memory_size"]))

    link_ld_file = os.path.join("__chips__", "link.ld")
    with open(link_ld_file, "w") as f:
        f.write("".join(link_ld))

def generate_header(settings):

    address = 0x80000008
    header = ["//Auto Generated Machine Description Header\n"]
    header = ["const unsigned int CLOCKS_PER_SEC = %u;\n"%settings["clocks_per_sec"]]

    #Add memory locations of outputs
    for output in settings["outputs"]:
        header.append("const unsigned int %s = 0x%x;\n"%(output, address));
        address += 4

    #Add memory locations of inputs
    for output in settings["inputs"]:
        header.append("const unsigned int %s = 0x%x;\n"%(output, address));
        address += 4

    machine_h = os.path.join("__chips__", "include", "machine.h")
    with open(machine_h, "w") as f:
        f.write("".join(header))

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
	j _end""".replace("MEM_SIZE", str(settings["memory_size"]-4))

    machine_h = os.path.join("__chips__", "start.S")
    with open(machine_h, "w") as f:
        f.write("".join(start_s))


def read_binfile(binfile):
    with open(binfile, "rb") as f:
        bindata = f.read()
    
    instructions = []
    for i in range(len(bindata) // 4):
        w = bindata[4 * i: 4 * i + 4]
        instructions.append(w[3] << 24 | w[2] << 16 | w[1] << 8 | w[0])

    return instructions

def c_compile(input_files, settings=default_settings):

    # Create a working folder to perform the build
    if os.path.exists("__chips__"):
        shutil.rmtree("__chips__")
    os.mkdir("__chips__")
    os.mkdir(os.path.join("__chips__", "include"))

    # generate machine specific header
    generate_header(settings)

    # generate machine specific startup code
    generate_start_code(settings)

    # generate machine specific link script
    generate_linker_script(settings)

    #Create a static include directory
    directory = os.path.abspath(__file__)
    directory = os.path.dirname(directory)
    include = os.path.join(directory, "include")
    local_include = " %s"%os.path.abspath(os.path.join("__chips__", "include"))
    input_files = [os.path.abspath(i) for i in input_files]
    link_script = "./link.ld"

    #Compile into an elf file
    compile_command=("/opt/riscv/bin/riscv32-unknown-elf-gcc -Os -I%s -I%s "
                     "-march=%s -mcmodel=medlow -ffunction-sections "
                     "-Wl,--gc-sections "
                     "-fdata-sections --specs=nosys.specs -nostartfiles "
                     "-T %s -o main.elf start.S %s")

    compile_command=compile_command%(
        local_include,
        include, 
        settings["march"],
        link_script, 
        " ".join(input_files), 
    )

    print(compile_command)
    
    #move into working directory
    starting_dir = os.getcwd()
    os.chdir("__chips__")

    try:

        #run compiler
        result = subprocess.call(compile_command, shell=True)
        if result != 0:
            raise CompileError

        #convert to binary file
        copy_command=("/opt/riscv/bin/riscv32-unknown-elf-objcopy -S -O binary"
                      " main.elf main.bin")
        result = subprocess.call(copy_command, shell=True)
        if result != 0:
            raise BinaryError

        #convert to a list of instructions
        instructions=read_binfile("main.bin")

    finally:
        os.chdir(starting_dir)


    return instructions
