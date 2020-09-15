from baremetal import *
from chips_v.utils import *


def decode(instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc):

    rs1 = instruction[19:15]
    rs2 = instruction[24:20]
    opcode = instruction[6:0]
    shamt = instruction[24:20]
    funct3 = instruction[14:12]

    opcode_is_immediate = (opcode == 0b0010011)
    opcode_is_lui = (opcode == 0b0110111)
    opcode_is_auipc = (opcode == 0b0010111)
    opcode_is_jal = (opcode == 0b1101111)
    opcode_is_jalr = (opcode == 0b1100111)

    # forward result of register that has just been written
    src1 = Signed(32).select(fwd1, src1, fwd_val)
    src2 = Signed(32).select(fwd2, src2, fwd_val)

    # x0 should always read 0
    src1 = Signed(32).select(rs1 == 0, src1, 0)
    src2 = Signed(32).select(rs2 == 0, src2, 0)

    # for register - register instructions use register values for A and B
    A = src1
    B = src2

    # for register - immediate instructions substitute B for an immediate
    B = Signed(32).select(opcode_is_immediate, src2,
                          Signed(32).constant(0) + instruction[31:20])
    signed = instruction[30]
    shift_amount = Unsigned(5).select(opcode_is_immediate, B[4:0], shamt)
    add_sub = instruction[30] & ~ opcode_is_immediate
    operation = funct3

    # for LUI instructions override ALU inputs
    # rd <= upper_immediate + 0
    A = Signed(32).select(
        opcode_is_lui, A, instruction[31:12].resize(32) << 12)
    B = Signed(32).select(
        opcode_is_lui, B, Signed(32).constant(0))
    operation = Unsigned(7).select(opcode_is_lui, operation, 0)
    add_sub = add_sub & ~ opcode_is_lui

    # for AUIPC instructions override ALU inputs
    # rd <= upper_immediate + this_pc
    A = Signed(32).select(
        opcode_is_auipc, A, instruction[31:12].resize(32) << 12)
    B = Signed(32).select(
        opcode_is_auipc, B, this_pc)
    operation = Unsigned(7).select(opcode_is_auipc, operation, 0)
    add_sub = add_sub & ~ opcode_is_auipc

    # for JAL/JALR instructions override ALU inputs
    # rd <= this_pc + 4
    A = Signed(32).select(
        opcode_is_jal | opcode_is_jalr, A, Signed(32).constant(4))
    B = Signed(32).select(
        opcode_is_jal | opcode_is_jalr, B, this_pc)
    operation = Unsigned(7).select(
        opcode_is_jal | opcode_is_jalr, operation, 0)
    add_sub = add_sub & ~ (opcode_is_jal | opcode_is_jalr)

    return src1, src2, A, B, operation, shift_amount, add_sub, signed


def decode_model(instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc):
    src1 = int32trunc(src1)
    src2 = int32trunc(src2)

    rs1 = get_slice(instruction, 19, 15)
    rs2 = get_slice(instruction, 24, 20)
    opcode = get_slice(instruction, 6, 0)

    if fwd1:
        src1 = int32trunc(fwd_val)
    if fwd2:
        src2 = int32trunc(fwd_val)
    if rs1 == 0:
        src1 = 0
    if rs2 == 0:
        src2 = 0

    if opcode == 0b0110111:  # LUI
        A = int32trunc(get_slice(instruction, 31, 12) << 12)
        B = int32trunc(0)
        operation = 0
        shift_amount = "don't_care"
        add_sub = 0
        signed = "don't_care"

    elif opcode == 0b0010111:  # AUIPC
        A = int32trunc(get_slice(instruction, 31, 12) << 12)
        B = int32trunc(this_pc)
        operation = 0
        shift_amount = "don't_care"
        add_sub = 0
        signed = "don't_care"

    elif opcode == 0b1101111:  # JAL
        A = 4
        B = int32trunc(this_pc)
        operation = 0
        shift_amount = "don't_care"
        add_sub = 0
        signed = "don't_care"

    elif opcode == 0b1100111:  # JALR
        A = 4
        B = int32trunc(this_pc)
        operation = 0
        shift_amount = "don't_care"
        add_sub = 0
        signed = "don't_care"

    elif opcode == 0b1100011:  # BEQ BNE BLT BGE BLTU BGEU
        A = "don't_care"
        B = "don't_care"
        operation = "don't_care"
        shift_amount = "don't_care"
        add_sub = "don't_care"
        signed = "don't_care"

    elif opcode == 0b0000011:  # LB LH LW LBU LHU
        A = "don't_care"
        B = "don't_care"
        operation = "don't_care"
        shift_amount = "don't_care"
        add_sub = "don't_care"
        signed = "don't_care"

    elif opcode == 0b0100011:  # SB SH SW
        A = "don't_care"
        B = "don't_care"
        operation = "don't_care"
        shift_amount = "don't_care"
        add_sub = "don't_care"
        signed = "don't_care"

    elif opcode == 0b0010011:  # ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI
        A = src1
        B = int32trunc(sign_extend(get_slice(instruction, 31, 20), 12))
        operation = get_slice(instruction, 14, 12)
        shift_amount = get_slice(instruction, 24, 20)
        add_sub = 0
        signed = get_slice(instruction, 30, 30)

    elif opcode == 0b0110011:  # ADD SUB SLL SLT SLTU XOR SRL SRA OR AND
        A = src1
        B = src2
        operation = get_slice(instruction, 14, 12)
        shift_amount = get_slice(instruction, 24, 20)
        add_sub = get_slice(instruction, 30, 30)
        signed = get_slice(instruction, 30, 30)

    else:
        print("unknown")

# 0001111 FENCE
# 1110011 ECALL
# 1110011 EBREAK

    return src1, src2, A, B, operation, shift_amount, add_sub, signed


def print_stim(stim):
    (instruction_stim, src1_stim, src2_stim, fwd1_stim, fwd2_stim,
     fwd_val_stim, this_pc_stim) = stim
    print("stimulus")
    print("--------")
    print(stim)
    print(("instruction", hex(instruction_stim)))
    print(("opcode", bin(get_slice(instruction_stim, 6, 0))))
    print(("long_immediate", bin(get_slice(instruction_stim, 31, 12))))
    print(("src1_stim", src1_stim))
    print(("src2_stim", src2_stim))


def compare(actual, expected):
    if expected == "don't_care":
        return False
    return actual != expected


def test():
    import itertools

    instruction = Unsigned(32).input("instruction")
    src1 = Signed(32).input("src1")
    src2 = Signed(32).input("src2")
    fwd1 = Boolean().input("fwd1")
    fwd2 = Boolean().input("fwd2")
    fwd_val = Signed(32).input("fwd_val")
    this_pc = Signed(32).input("this_pc")
    inputs = [instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc]

    (src1_out, src2_out, A, B, operation, shift_amount, add_sub,
     issigned) = decode(*inputs)

    opcodes = [
        0b0110111,  # LUI
        0b0010111,  # AUIPC
        0b1101111,  # JAL
        0b1100111,  # JALR
        0b1100011,  # BEQ BNE BLT BGE BLTU BGEU
        0b0000011,  # LB LH LW LBU LHU
        0b0100011,  # SB SH SW
        0b0010011,  # ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI
        0b0110011  # ADD SUB SLL SLT SLTU XOR SRL SRA OR AND
    ]

    instruction_stim = []
    functions = [0, 1, 6, 7, 0x7ffffffe, 0x7fffffff,
                 0x80000000, 0xfffffffe, 0xffffffff]
    for opcode in opcodes:
        for funct3 in functions:
            for rs1 in [0, 31]:
                for rs2 in [0, 31]:
                    for signed in [0, 1]:
                        instruction_stim.append(
                            opcode | (rs1 << 15) |
                            (rs2 << 20) | (funct3 << 12) |
                            (signed << 30))

    src1_stim = [0x00000000, 0x00000001, 0x7ffffffe,
                 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff]
    src2_stim = src1_stim + [0b10000, 0b01000, 0b11111, 0b01111]
    fwd1_stim = list(range(2))
    fwd2_stim = list(range(2))
    fwd_val_stim = src1_stim
    this_pc_stim = src1_stim

    stimulus = itertools.product(
        instruction_stim, src1_stim, src2_stim, fwd1_stim, fwd2_stim,
        fwd_val_stim, this_pc_stim)
    stimulus = list(stimulus)
    # random.shuffle(stimulus)
    for idx, stim in enumerate(stimulus):
        if idx % 10000 == 0:
            print("testing decode", 100 * idx // len(stimulus), "%")
        for i, v in zip(inputs, stim):
            i.set(v)
        actual_src1 = src1_out.get()
        actual_src2 = src2_out.get()
        actual_A = A.get()
        actual_B = B.get()
        actual_operation = operation.get()
        actual_shift_amount = shift_amount.get()
        actual_add_sub = add_sub.get()
        actual_signed = issigned.get()
        (expected_src1, expected_src2, expected_A, expected_B,
         expected_operation, expected_shift_amount, expected_add_sub,
         expected_signed) = decode_model(*stim)

        if (compare(actual_src1, expected_src1) |
            compare(actual_src2, expected_src2) |
            compare(actual_A, expected_A) |
            compare(actual_B, expected_B) |
            compare(actual_operation, expected_operation) |
            compare(actual_add_sub, expected_add_sub) |
                compare(actual_signed, expected_signed)):

            print("fail")
            print_stim(stim)
            print("response (actual, expected)")
            print("---------------------------")
            print(("src1", hex(actual_src1), hex(expected_src1)))
            print(("src2", hex(actual_src2), hex(expected_src2)))
            print(("A", hex(actual_A), hex(expected_A)))
            print(("B", hex(actual_B), hex(expected_B)))
            print(("operation", hex(actual_operation),
                   hex(expected_operation)))
            print(("shift_amount", hex(actual_shift_amount),
                   hex(expected_shift_amount)))
            print(("add_sub", hex(actual_add_sub), hex(expected_add_sub)))
            print(("signed", hex(actual_signed), hex(expected_signed)))
            return False

    return True
