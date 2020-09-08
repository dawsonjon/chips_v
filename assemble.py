from utils import *


def store(funct3, address_offset, address_reg, data_reg):

    rs1 = address_reg & 0x1f
    rs2 = data_reg & 0x1f
    immediate1 = get_slice(address_offset & 0xfff, 11, 5)
    immediate2 = get_slice(address_offset & 0xfff, 4, 0)
    opcode = 0b0100011  # SB SH SW
    instruction = opcode | (funct3 << 12) | (immediate1 << 25) | (
        immediate2 << 7) | (rs1 << 15) | (rs2 << 20)

    return instruction & 0xffffffff


def sb(address_offset, address_reg, data_reg):
    return store(0, address_offset, address_reg, data_reg)


def sh(address_offset, address_reg, data_reg):
    return store(1, address_offset, address_reg, data_reg)


def sw(address_offset, address_reg, data_reg):
    return store(2, address_offset, address_reg, data_reg)


def load(funct3, address_offset, address_reg, result_reg):

    rs1 = address_reg & 0x1f
    rd = result_reg & 0x1f
    immediate = get_slice(address_offset & 0xfff, 11, 0)
    opcode = 0b0000011  # LB LH LW LBU LHU
    instruction = opcode | (funct3 << 12) | (
        immediate << 20) | (rd << 7) | (rs1 << 15)

    return instruction & 0xffffffff


def lb(address_offset, address_reg, result_reg):
    return load(0, address_offset, address_reg, result_reg)


def lh(address_offset, address_reg, result_reg):
    return load(1, address_offset, address_reg, result_reg)


def lw(address_offset, address_reg, result_reg):
    return load(2, address_offset, address_reg, result_reg)


def lbu(address_offset, address_reg, result_reg):
    return load(4, address_offset, address_reg, result_reg)


def lhu(address_offset, address_reg, result_reg):
    return load(1, address_offset, address_reg, result_reg)


def immediate_instruction(funct3, immediate, reg, result_reg):
    rs1 = reg & 0x1f
    rd = result_reg & 0x1f
    immediate = immediate & 0xfff
    funct3 = funct3 & 0x7f
    opcode = 0b0010011
    instruction = opcode | (immediate << 20) | (
        rd << 7) | (rs1 << 15) | (funct3 << 12)
    return instruction & 0xffffffff


def addi(immediate, reg, result_reg):
    return immediate_instruction(0, immediate, reg, result_reg)


def register_instruction(funct3, reg, reg2, result_reg, special):
    rs1 = reg & 0x1f
    rs2 = reg2 & 0x1f
    rd = result_reg & 0x1f
    funct3 = funct3 & 0x7f
    special = special & 1
    opcode = 0b0110011
    instruction = opcode | (rs2 << 20) | (rd << 7) | (
        rs1 << 15) | (funct3 << 12) | (special << 30)
    return instruction & 0xffffffff


def add(reg, reg2, result_reg):
    return register_instruction(
        funct3=0, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def sub(reg, reg2, result_reg):
    return register_instruction(
        funct3=0, reg=reg, reg2=reg2, result_reg=result_reg, special=1)


def sll(reg, reg2, result_reg):
    return register_instruction(
        funct3=1, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def slt(reg, reg2, result_reg):
    return register_instruction(
        funct3=2, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def sltu(reg, reg2, result_reg):
    return register_instruction(
        funct3=3, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def xor(reg, reg2, result_reg):
    return register_instruction(
        funct3=4, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def srl(reg, reg2, result_reg):
    return register_instruction(
        funct3=5, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def sra(reg, reg2, result_reg):
    return register_instruction(
        funct3=5, reg=reg, reg2=reg2, result_reg=result_reg, special=1)


def or_(reg, reg2, result_reg):
    return register_instruction(
        funct3=6, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def and_(reg, reg2, result_reg):
    return register_instruction(
        funct3=6, reg=reg, reg2=reg2, result_reg=result_reg, special=0)


def jal(immediate, result_reg):
    rd = result_reg & 0x1f
    opcode = 0b1101111

    immediate = immediate & 0x1fffff  # (21 bit immediate)
    instruction = (
        get_slice(immediate, 20, 20) << 31 |
        get_slice(immediate, 19, 12) << 12 |
        get_slice(immediate, 11, 11) << 20 |
        get_slice(immediate, 10, 1) << 21
    )
    instruction |= opcode | (rd << 7)

    return instruction


def jalr(immediate, reg, result_reg):
    rd = result_reg & 0x1f
    rs1 = reg & 0x1f
    opcode = 0b1100111

    immediate = immediate & 0xfff  # (12 bit immediate)
    instruction = immediate << 20
    instruction |= opcode | (rd << 7) | (rs1 << 15)

    return instruction


def auipc(immediate, result_reg):
    rd = result_reg & 0x1f
    immediate = get_slice(immediate, 31, 12)
    opcode = 0b0010111
    instruction = opcode | (immediate << 12) | (rd << 7)
    return instruction & 0xffffffff


def lui(immediate, result_reg):
    rd = result_reg & 0x1f
    immediate = get_slice(immediate, 31, 12)
    opcode = 0b0110111
    instruction = opcode | (immediate << 12) | (rd << 7)
    return instruction & 0xffffffff


def branch(funct3, immediate, reg, reg2):
    rs1 = reg & 0x1f
    rs2 = reg2 & 0x1f
    opcode = 0b1100011
    funct3 = funct3 & 0x7
    immediate = immediate & 0x1fff  # (12 bit immediate)

    instruction = (
        get_slice(immediate, 12, 12) << 31 |
        get_slice(immediate, 10, 5) << 25 |
        get_slice(immediate, 4, 1) << 8 |
        get_slice(immediate, 11, 11) << 7
    )
    instruction |= opcode | (rs2 << 20) | (rs1 << 15) | (funct3 << 12)

    return instruction


def beq(immediate, reg, reg2):
    return branch(0, immediate, reg, reg2)


def bne(immediate, reg, reg2):
    return branch(1, immediate, reg, reg2)
