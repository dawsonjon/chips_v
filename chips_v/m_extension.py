"""A co-processor containing hard multiplier and divider to implement optional
m extension to RISC-V CPU"""

from chips_v.divider import divider
from chips_v.multiplier import multiplier


def m_extension(clk, A, B, instruction):

    funct3 = instruction[14:12]
    opcode = instruction[6:0]

    opcode_is_m = (opcode == 0b0110011) & instruction[25]
    funct3_is_mul = (funct3 == 0b000) & opcode_is_m
    funct3_is_mulh = (funct3 == 0b001) & opcode_is_m
    funct3_is_mulhsu = (funct3 == 0b010) & opcode_is_m
    funct3_is_mulhu = (funct3 == 0b011) & opcode_is_m
    funct3_is_div = (funct3 == 0b100) & opcode_is_m
    funct3_is_divu = (funct3 == 0b101) & opcode_is_m
    funct3_is_rem = (funct3 == 0b110) & opcode_is_m
    funct3_is_remu = (funct3 == 0b111) & opcode_is_m

    # Implement division and modulo
    divider_go = opcode_is_m & funct3[2]
    div_mod = funct3[1]
    divide_is_signed = ~funct3[0]

    div, mod, div_done, _ = divider(clk, A, B, divide_is_signed, divider_go)

    # implement multiplication
    mul_go = opcode_is_m & ~funct3[2]
    a_signed = funct3_is_mul | funct3_is_mulh | funct3_is_mulhsu
    b_signed = funct3_is_mul | funct3_is_mulh

    prod_h, prod, mul_done, _ = multiplier(clk, A, B, a_signed, b_signed, mul_go)

    # select hi/low multiplication result of division/modulo result
    result = A.subtype.select(
        divider_go,
        A.subtype.select(funct3_is_mul, prod_h, prod),
        A.subtype.select(div_mod, div, mod),
    )
    done = A.subtype.select(divider_go, mul_done & opcode_is_m, div_done & opcode_is_m)

    return result, done & opcode_is_m, opcode_is_m & ~done
