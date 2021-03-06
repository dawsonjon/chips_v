from baremetal import *
from chips_v.alu import ALU_model, alu
from chips_v.utils import *


def execute(
    instruction,
    src1,
    src2,
    A,
    B,
    operation,
    add_sub,
    shift_amount,
    is_signed,
    data_in,
    this_pc,
):

    opcode = instruction[6:0]
    funct3 = instruction[14:12]

    opcode_is_immediate = opcode == 0b0010011
    opcode_is_register = opcode == 0b0110011
    opcode_is_lui = opcode == 0b0110111
    opcode_is_auipc = opcode == 0b0010111
    opcode_is_jal = opcode == 0b1101111
    opcode_is_jalr = opcode == 0b1100111
    opcode_is_load = opcode == 0b0000011
    opcode_is_store = opcode == 0b0100011
    opcode_is_branch = opcode == 0b1100011

    # ALU
    write_data = alu(A, B, operation, add_sub, shift_amount, is_signed)
    write_enable = (
        opcode_is_immediate
        | opcode_is_register
        | opcode_is_jal
        | opcode_is_jalr
        | opcode_is_lui
        | opcode_is_auipc
        | opcode_is_load
    )

    # Implement load and store instructions
    address_offset = Signed(32).select(
        opcode_is_store, instruction[31:20], instruction[31:25].cat(instruction[11:7])
    )
    address_out = unsigned(src1 + signed(address_offset))
    byte_address = unsigned(address_out[1:0])
    hword_address = unsigned(address_out[1])

    byte = Unsigned(8).select(
        byte_address, data_in[7:0], data_in[15:8], data_in[23:16], data_in[31:24]
    )
    hword = Unsigned(16).select(hword_address, data_in[15:0], data_in[31:16])
    word = data_in

    write_data = Signed(32).select(
        opcode_is_load,
        write_data,
        Signed(32).select(
            funct3,
            signed(byte).resize(32),  # LB
            signed(hword).resize(32),  # LH
            data_in,  # LW
            Signed(32).constant(0),
            byte.resize(32),  # LBU
            hword.resize(32),  # LHU
            Signed(32).constant(0),
            Signed(32).constant(0),
        ),
    )

    byte = unsigned(src2[7:0]).resize(32)
    hword = unsigned(src2[15:0]).resize(32)
    word = unsigned(src2)
    data_out = Unsigned(32).select(
        funct3,
        Unsigned(32).select(
            byte_address, byte, byte << 8, byte << 16, byte << 24
        ),  # SB
        Unsigned(32).select(hword_address, hword, hword << 16),  # SH
        unsigned(word),  # SW
        Unsigned(32).constant(0),
        Unsigned(32).constant(0),
        Unsigned(32).constant(0),
        Unsigned(32).constant(0),
        Unsigned(32).constant(0),
    )

    byte_enable = Unsigned(4).select(
        funct3,
        Unsigned(4).constant(1) << unsigned(address_out[1:0]),  # SB
        Unsigned(4).constant(3) << unsigned(address_out[1]),  # SH
        Unsigned(4).constant(15),  # SW
        Unsigned(4).constant(0),
        Unsigned(4).constant(0),
        Unsigned(4).constant(0),
        Unsigned(4).constant(0),
        Unsigned(4).constant(0),
    )
    data_valid = opcode_is_load | opcode_is_store
    write_read = unsigned(opcode_is_store)

    # implement branch instructions
    take_branch = (
        opcode_is_jal
        | opcode_is_jalr
        | Boolean().select(
            opcode_is_branch,
            0,
            Boolean().select(
                funct3,
                src1 == src2,
                src1 != src2,
                0,
                0,
                src1 < src2,
                src1 >= src2,
                unsigned(src1) < unsigned(src2),
                unsigned(src1) >= unsigned(src2),
            ),
        )
    )

    branch_offset = signed(
        cat(
            instruction[31],
            instruction[7],
            instruction[30:25],
            instruction[11:8],
            Unsigned(1).constant(0),
        )
    ).resize(32)

    jal_offset = signed(
        cat(
            instruction[31],
            instruction[19:12],
            instruction[20],
            instruction[30:21],
            Unsigned(1).constant(0),
        )
    ).resize(32)

    branch_address = (
        Unsigned(32).select(opcode_is_jal, branch_offset, jal_offset) + this_pc
    )

    branch_address = Unsigned(32).select(
        opcode_is_jalr,
        branch_address,
        (src1 + signed(instruction[31:20]).resize(32)) & 0xFFFFFFFE,
    )

    return (
        # data to write to registers
        write_data,  # data to write back to registers
        write_enable,  # write enable to registers
        # data bus
        data_out,
        address_out,
        byte_enable,
        data_valid,
        write_read,
        # branch info
        take_branch,
        branch_address,
    )


def execute_model(
    instruction,
    src1,
    src2,
    A,
    B,
    operation,
    add_sub,
    shift_amount,
    is_signed,
    data_in,
    this_pc,
):

    src1 = int32trunc(src1)
    src2 = int32trunc(src2)
    A = int32trunc(A)
    B = int32trunc(B)
    opcode = get_slice(instruction, 6, 0)
    funct3 = get_slice(instruction, 14, 12)

    if opcode == 0b0110111:  # LUI

        write_data = int32trunc(A + B)  # assume A=upper, B=0
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 0
        branch_address = "don't_care"
        write_read = "don't_care"

    elif opcode == 0b0010111:  # AUIPC
        write_data = int32trunc(A + B)  # assume A=upper, B=pc
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 0
        branch_address = "don't_care"
        write_read = "don't_care"

    elif opcode == 0b1101111:  # JAL
        write_data = int32trunc(A + B)  # assume A is pc and B is 4
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 1
        branch_address = this_pc + (
            get_slice(instruction, 30, 21) << 1
            | get_slice(instruction, 20, 20) << 11
            | get_slice(instruction, 19, 12) << 12
            | get_slice(instruction, 31, 31) << 20
        )
        branch_address &= 0xFFFFFFFF
        write_read = "don't_care"

    elif opcode == 0b1100111:  # JALR
        write_data = int32trunc(A + B)
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 1
        branch_address = src1 + get_slice(instruction, 31, 20)
        branch_address &= 0xFFFFFFFE
        write_read = "don't_care"

    elif opcode == 0b1100011:  # BEQ BNE BLT BGE BLTU BGEU

        write_data = "don't_care"
        write_enable = 0
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = [
            src1 == src2,
            src1 != src2,
            "don't_care",
            "don't_care",
            src1 < src2,
            src1 >= src2,
            src1 & 0xFFFFFFFF < src2 & 0xFFFFFFFF,
            src1 & 0xFFFFFFFF >= src2 & 0xFFFFFFFF,
        ][funct3]
        branch_address = this_pc + (
            get_slice(instruction, 31, 31) << 12
            | get_slice(instruction, 7, 7) << 11
            | get_slice(instruction, 30, 25) << 5
            | get_slice(instruction, 11, 8) << 1
        )
        write_read = "don't_care"

    elif opcode == 0b0000011:  # LB LH LW LBU LHU
        data_in = int32trunc(data_in)
        address_out = (
            int32trunc(src1 + sign_extend(get_slice(instruction, 31, 20), 12))
            & 0xFFFFFFFF
        )
        byte_address = address_out & 0x3
        byte = [
            get_slice(data_in, 7, 0),
            get_slice(data_in, 15, 8),
            get_slice(data_in, 23, 16),
            get_slice(data_in, 31, 24),
        ][byte_address]
        hword_address = byte_address >> 1
        hword = [get_slice(data_in, 15, 0), get_slice(data_in, 31, 16)][hword_address]
        write_data = [
            sign_extend(byte, 8),
            sign_extend(hword, 16),
            data_in,
            "don't_care",
            byte,
            hword,
            "don't_care",
            "don't_care",
        ][funct3]
        write_enable = 1
        data_out = "don't_care"
        byte_enable = [
            1 << byte_address,
            3 << hword_address,
            15,
            "don't_care",
            1 << byte_address,
            3 << hword_address,
            "don't_care",
            "don't_care",
        ][funct3]
        data_valid = 1
        take_branch = 0
        branch_address = "don't_care"
        write_read = 0

    elif opcode == 0b0100011:  # SB SH SW
        address_out = (
            int32trunc(
                src1
                + sign_extend(
                    get_slice(instruction, 31, 25) << 5
                    | (get_slice(instruction, 11, 7)),
                    12,
                )
            )
            & 0xFFFFFFFF
        )

        # store operations don't write to any registers
        write_data = "don't_care"
        write_enable = 0

        # position byte in correct portion of data bus
        byte_address = address_out & 0x3
        byte = [
            get_slice(src2, 7, 0),
            get_slice(src2, 7, 0) << 8,
            get_slice(src2, 7, 0) << 16,
            get_slice(src2, 7, 0) << 24,
        ][byte_address] & 0xFFFFFFFF

        # position hword in correct portion of data bus
        hword_address = byte_address >> 1
        hword = [get_slice(src2, 15, 0), get_slice(src2, 15, 0) << 16][
            hword_address
        ] & 0xFFFFFFFF

        # use whole word
        word = src2 & 0xFFFFFFFF

        # select for byte, hword or word store
        data_out = [
            byte,
            hword,
            word,
            "don't_care",
            "don't_care",
            "don't_care",
            "don't_care",
            "don't_care",
        ][funct3]

        # work out which bytes get written
        byte_enable = [
            1 << byte_address,
            3 << hword_address,
            15,
            "don't_care",
            "don't_care",
            "don't_care",
            "don't_care",
            "don't_care",
        ][funct3]
        data_valid = 1
        take_branch = 0
        branch_address = "don't_care"
        write_read = 1

    elif opcode == 0b0010011:  # ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI
        write_data = ALU_model(
            int32trunc(A), int32trunc(B), operation, add_sub, shift_amount, is_signed
        )
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 0
        branch_address = "don't_care"
        write_read = "don't_care"

    elif opcode == 0b0110011:  # ADD SUB SLL SLT SLTU XOR SRL SRA OR AND
        write_data = ALU_model(
            int32trunc(A), int32trunc(B), operation, add_sub, shift_amount, is_signed
        )
        write_enable = 1
        data_out = "don't_care"
        address_out = "don't_care"
        byte_enable = "don't_care"
        data_valid = 0
        take_branch = 0
        branch_address = "don't_care"
        write_read = "don't_care"

    else:
        print("unknown")

    return (
        # data to write to registers
        write_data,  # data to write back to registers
        write_enable,  # write enable to registers
        # data bus
        data_out,
        address_out,
        byte_enable,
        data_valid,
        # branch info
        take_branch,
        branch_address,
        write_read,
    )


def compare(actual, expected):
    if expected == "don't_care":
        return False
    return actual != expected


def test():
    import itertools

    instruction = Unsigned(32).input("instruction")
    src1 = Signed(32).input("src1")
    src2 = Signed(32).input("src2")
    A = Signed(32).input("A")
    B = Signed(32).input("B")
    operation = Unsigned(3).input("operation")
    add_sub = Boolean().input("add_sub")
    shift_amount = Unsigned(5).input("shift_amount")
    is_signed = Boolean().input("is_signed")
    data_in = Unsigned(32).input("data_in")
    this_pc = Unsigned(32).input("this_pc")

    inputs = [
        instruction,
        src1,
        src2,
        A,
        B,
        operation,
        add_sub,
        shift_amount,
        is_signed,
        data_in,
        this_pc,
    ]

    (
        # data to write to registers
        write_data,  # data to write back to registers
        write_enable,  # write enable to registers
        # data bus
        data_out,
        address_out,
        byte_enable,
        data_valid,
        write_read,
        # branch info
        take_branch,
        branch_address,
    ) = execute(
        instruction,
        src1,
        src2,
        A,
        B,
        operation,
        add_sub,
        shift_amount,
        is_signed,
        data_in,
        this_pc,
    )

    # generate stimulus
    # 0b0110111, # LUI
    # 0b0010111, # AUIPC
    # 0b1101111, #JAL
    # 0b1100111, #JALR
    # 0b1100011, #BEQ BNE BLT BGE BLTU BGEU
    # 0b0000011, #LB LH LW LBU LHU
    # 0b0100011, #SB SH SW
    # 0b0010011, #ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI
    # 0b0110011  #ADD SUB SLL SLT SLTU XOR SRL SRA OR AND

    # immediate instructions
    instruction_stim = []
    opcode = 0b0010011  # ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0xAAAAAAAA]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = list(range(8))
    add_sub_stim = [0, 1]
    shift_amount_stim = [0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111, 0b01111]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = [0x55555555]

    immediate_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # register instructions
    instruction_stim = []
    opcode = 0b0110011  # ADD SUB SLL SLT SLTU XOR SRL SRA OR AND
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0xAAAAAAAA]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = list(range(8))
    add_sub_stim = [0, 1]
    shift_amount_stim = [0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111, 0b01111]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = [0x55555555]

    register_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # LUI instructions
    instruction_stim = []
    opcode = 0b0110111  # LUI
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0xAAAAAAAA]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = [0x55555555]

    lui_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # AUIPC instructions
    instruction_stim = []
    opcode = 0b0010111  # AUIPC
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0xAAAAAAAA]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = A_stim

    auipc_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # JAL instructions
    instruction_stim = []
    opcode = 0b1101111  # JAL
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = A_stim

    jal_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # JALR instructions
    instruction_stim = []
    opcode = 0b1100111  # JALR
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    src2_stim = [0xFFFFFFFF]
    A_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    B_stim = A_stim
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = A_stim

    jalr_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # branch instructions
    instruction_stim = []
    opcode = 0b1100011  # BEQ BNE BLT BGE BLTU BGEU
    for funct3 in [0, 1, 6, 7]:
        instruction_stim.append(opcode | (funct3 << 12))

    src1_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    src2_stim = src1_stim
    A_stim = [0x55555555]
    B_stim = [0x55555555]
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = A_stim

    branch_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # load instructions
    instruction_stim = []
    opcode = 0b0000011  # LB LH LW LBU LHU
    for immediate in [0x000, 0x001, 0x7FE, 0x7FF, 0x800, 0xFFE, 0xFFF]:
        for funct3 in [0, 1, 6, 7]:
            instruction_stim.append(opcode | (funct3 << 12) | (immediate << 12))

    src1_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    src2_stim = src1_stim
    A_stim = [0x55555555]
    B_stim = [0x55555555]
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [1 << i for i in range(32)]
    this_pc_stim = A_stim

    load_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    # store instructions
    instruction_stim = []
    opcode = 0b0100011  # SB SH SW
    for immediate1 in [0x00, 0x01, 0x3E, 0x3F, 0x40, 0x7E, 0x7F]:
        for immediate2 in [0x00, 0x01, 0x0E, 0x0F, 0x10, 0x1E, 0x1F]:
            for funct3 in [0, 1, 6, 7]:
                instruction_stim.append(
                    opcode | (funct3 << 12) | (immediate1 << 25) | (immediate2 << 7)
                )

    src1_stim = [0x00000000, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    src2_stim = src1_stim
    A_stim = [0x55555555]
    B_stim = [0x55555555]
    operation_stim = [0]  # decoder should guarantee this
    add_sub_stim = [0]  # decoder should guarantee this
    shift_amount_stim = [0b10101]
    is_signed_stim = [0, 1]
    data_in_stim = [0x55555555]
    this_pc_stim = A_stim

    store_stimulus = list(
        itertools.product(
            instruction_stim,
            src1_stim,
            src2_stim,
            A_stim,
            B_stim,
            operation_stim,
            add_sub_stim,
            shift_amount_stim,
            is_signed_stim,
            data_in_stim,
            this_pc_stim,
        )
    )

    stimulus = (
        store_stimulus
        + load_stimulus
        + immediate_stimulus
        + register_stimulus
        + branch_stimulus
        + lui_stimulus
        + jal_stimulus
        + auipc_stimulus
        + jalr_stimulus
        + branch_stimulus
    )

    for idx, stim in enumerate(stimulus):
        if idx % 10000 == 0:
            print("testing execute", 100 * idx // len(stimulus), "%")
        for i, v in zip(inputs, stim):
            i.set(v)

        actual_write_data = write_data.get()
        actual_write_enable = write_enable.get()
        actual_data_out = data_out.get()
        actual_address_out = address_out.get()
        actual_byte_enable = byte_enable.get()
        actual_data_valid = data_valid.get()
        actual_take_branch = take_branch.get()
        actual_branch_address = branch_address.get()
        actual_write_read = write_read.get()

        (
            expected_write_data,
            expected_write_enable,
            expected_data_out,
            expected_address_out,
            expected_byte_enable,
            expected_data_valid,
            expected_take_branch,
            expected_branch_address,
            expected_write_read,
        ) = execute_model(*stim)

        def shex(a):
            try:
                return hex(a)
            except TypeError:
                return a

        if (
            compare(actual_write_data, expected_write_data)
            | compare(actual_write_enable, expected_write_enable)
            | compare(actual_data_out, expected_data_out)
            | compare(actual_address_out, expected_address_out)
            | compare(actual_byte_enable, expected_byte_enable)
            | compare(actual_data_valid, expected_data_valid)
            | compare(actual_take_branch, expected_take_branch)
            | compare(actual_branch_address, expected_branch_address)
            | compare(actual_write_read, expected_write_read)
        ):
            print("fail")
            print("stimulus")
            print("---------------------------")
            print(("instruction", hex(stim[0])))
            print(("upper immediate", hex(get_slice(stim[0], 31, 12))))
            print(
                (
                    "store immediate",
                    hex(get_slice(stim[0], 31, 25) << 5 | get_slice(stim[0], 11, 7)),
                )
            )
            print(("opcode", bin(get_slice(stim[0], 6, 0))))
            print(("funct3", bin(get_slice(stim[0], 14, 12))))
            print(("src1", hex(stim[1])))
            print(("src2", hex(stim[2])))
            print(("A", hex(stim[3])))
            print(("B", hex(stim[4])))
            print(("this_pc", hex(stim[10])))
            print("response (actual, expected)")
            print("---------------------------")
            print(("write_data", shex(actual_write_data), shex(expected_write_data)))
            print(
                ("write_enable", shex(actual_write_enable), shex(expected_write_enable))
            )
            print(("data_out", shex(actual_data_out), shex(expected_data_out)))
            print(("address_out", shex(actual_address_out), shex(expected_address_out)))
            print(("byte_enable", shex(actual_byte_enable), shex(expected_byte_enable)))
            print(("data_valid", shex(actual_data_valid), shex(expected_data_valid)))
            print(("write_read", shex(actual_write_read), shex(expected_write_read)))
            print(("take_branch", shex(actual_take_branch), shex(expected_take_branch)))
            print(
                (
                    "branch_address",
                    shex(actual_branch_address),
                    shex(expected_branch_address),
                )
            )
            return False
    return True
