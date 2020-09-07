# GCC toolchain programs.
CC = /opt/riscv/bin/riscv32-unknown-elf-gcc
OD = riscv32-unknown-elf-objdump
OC = /opt/riscv/bin/riscv32-unknown-elf-objcopy

# Assembly directives.
# Don't perform optimizations.
ASFLAGS += -O0
# Report all warnings.
ASFLAGS += -Wall
# Just the core RV32I ISA.
ASFLAGS += -march=rv32i
# No extra startup code.
ASFLAGS += -nostartfiles
ASFLAGS += -nostdlib
ASFLAGS += --specs=nosys.specs
ASFLAGS += -Wl,-Tlink.ld

# Source files.
SRC  = ./I-ADD-01.S
SRC += ./I-ADDI-01.S
SRC += ./I-AND-01.S
SRC += ./I-ANDI-01.S
SRC += ./I-AUIPC-01.S
SRC += ./I-BEQ-01.S
SRC += ./I-BGE-01.S
SRC += ./I-BGEU-01.S
SRC += ./I-BLT-01.S
SRC += ./I-BLTU-01.S
SRC += ./I-BNE-01.S
SRC += ./I-DELAY_SLOTS-01.S
SRC += ./I-EBREAK-01.S
SRC += ./I-ECALL-01.S
SRC += ./I-ENDIANESS-01.S
SRC += ./I-IO-01.S
SRC += ./I-JAL-01.S
SRC += ./I-JALR-01.S
SRC += ./I-LB-01.S
SRC += ./I-LBU-01.S
SRC += ./I-LH-01.S
SRC += ./I-LHU-01.S
SRC += ./I-LW-01.S
SRC += ./I-LUI-01.S
SRC += ./I-MISALIGN_JMP-01.S
SRC += ./I-MISALIGN_LDST-01.S
SRC += ./I-NOP-01.S
SRC += ./I-OR-01.S
SRC += ./I-ORI-01.S
SRC += ./I-RF_size-01.S
SRC += ./I-RF_width-01.S
SRC += ./I-RF_x0-01.S
SRC += ./I-SB-01.S
SRC += ./I-SH-01.S
SRC += ./I-SW-01.S
SRC += ./I-SLL-01.S
SRC += ./I-SLLI-01.S
SRC += ./I-SLT-01.S
SRC += ./I-SLTI-01.S
SRC += ./I-SLTIU-01.S
SRC += ./I-SLTU-01.S
SRC += ./I-SRA-01.S
SRC += ./I-SRAI-01.S
SRC += ./I-SRL-01.S
SRC += ./I-SRLI-01.S
SRC += ./I-SUB-01.S
SRC += ./I-XOR-01.S

# Binary images to build.
OBJS = $(SRC:.S=.hex)

# Default rule to build all test files.
#.PHONY: all
all: $(OBJS)
	# Rule to assemble assembly files.

%.hex: %.bin 
	python3 makehex.py $< $@

%.bin: %.o
	$(OC) -S -O binary $< $@

%.o: %.S
	$(CC) -x assembler-with-cpp $(ASFLAGS) $< -o $@

# Rule to clear out generated build files.
#.PHONY: clean
#clean:



#/opt/riscv/bin/riscv32-unknown-elf-gcc --specs=nosys.specs -O0 -Wall -nostartfiles -nostdlib -Tlink.ld -o test.elf I-ADD-01.S
#/opt/riscv/bin/riscv32-unknown-elf-objdump -d test.elf
#/opt/riscv/bin/riscv32-unknown-elf-objcopy -S -O binary test.elf test.bin
#python3 makehex.py test.bin test.hex
