def m_extension(clk, A, B, instruction):

    funct3 = instruction[14:12]
    opcode = instruction[6:0]

    opcode_is_m = (opcode == 0b0110011)
    funct3_is_mul = (funct3 == 0b000) & opcode_is_m
    funct3_is_mulh = (funct3 == 0b001) & opcode_is_m
    funct3_is_mulhsu = (funct3 == 0b010) & opcode_is_m
    funct3_is_mulhu = (funct3 == 0b011) & opcode_is_m
    funct3_is_div = (funct3 == 0b100) & opcode_is_m
    funct3_is_divu = (funct3 == 0b101) & opcode_is_m
    funct3_is_rem = (funct3 == 0b110) & opcode_is_m
    funct3_is_remu = (funct3 == 0b111) & opcode_is_m

    divider_go = opcode_m & funct3[2]
    div_mod = funct3[1]
    divide_is_signed = ~funct3[0]
    div, mod, div_done, _ = sdivider(clk, A, B, divide_is_signed, divider_go)

    divider_go = (funct3_is_mul | funct3_is_divu |
                  funct3_is_mod | funct3_is_modu)
    mul = A * B

    result = A.subtype.select(divider_go,
                              A.subtype.select(h_l,
                                               prod,
                                               prodh
                                               ),
                              A.subtype.select(div_mod,
                                               div,
                                               mod
                                               )
                              )
    done = A.subtype.select(div_mul, mul_done, div_done)

    return result, done
