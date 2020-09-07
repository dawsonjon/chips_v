from baremetal import *


def unsigned(a):
	return Unsigned(a.subtype.bits).constant(0)+a

def signed(a):
	return Signed(a.subtype.bits).constant(0)+a

def int32trunc(a):
    signed = a & 0x80000000
    if signed:
        return (a & 0xffffffff) | ~0xffffffff
    else:
        return (a & 0xffffffff)

def get_slice(a, u, l):
    mask = (1 << (u + 1))-1
    return (a & mask) >> l

def sign_extend(a, old_bits):
    signed = a & (1<<(old_bits-1))
    mask = (1 << old_bits)-1
    if signed:
        return a | ~mask
    else:
        return a

def register(clk, en, *args):
    return [i.subtype.register(clk, en=en, init=0, d=i) for i in args]

def shex(a):
    try:
        return hex(a & 0xffffffff)
    except:
        return a

def sbin(a):
    try:
        return bin(a)
    except:
        return a

def print_instruction(instruction):
    opcode = get_slice(instruction, 6, 0)
    print(hex(instruction), "opcode", bin(opcode), end=' ') 
    funct3 = get_slice(instruction, 14, 12)
    if opcode == 0b0110111:
        print("LUI")
    elif opcode == 0b0010111:
        print("AUIPC")
    elif opcode == 0b1101111:
        print("JAL")
    elif opcode == 0b1100111:
        print("JALR")
    elif opcode == 0b1100011:
        print([
        "BEQ",
        "BNE",
        None, 
        None, 
        "BLT",
        "BGE",
        "BLTU",
        "BGEU",
        ][funct3])
    elif opcode == 0b0000011:
        print([
        "LB",
        "LH",
        "LW",
        None,
        "LBU",
        "LHU",
        ][funct3], "offset", shex(get_slice(instruction, 31, 20)), "rs1", get_slice(instruction, 19, 15), "rd", get_slice(instruction, 11, 7))
    elif opcode == 0b0100011:
        print([
        "SB",
        "SH",
        "SW",
        ][funct3])
    elif opcode == 0b0010011:
        print([
        "ADDI",
        "SLLI",
        "SLTI",
        "SLTIU",
        "XORI",
        "SRLI/SRAI",
        "ORI",
        "ANDI",
        ][funct3], "immediate:", shex(get_slice(instruction, 31, 20)), "rs1", get_slice(instruction, 19, 15), "rd:", get_slice(instruction, 11, 7))
    elif opcode == 0b0110011:
       print([
           "ADD/SUB",
           "SLL",
           "SLT",
           "SLTU",
           "XOR",
           "SRL/SRA",
           "OR",
           "AND",
    ][funct3])
    else:
        print("unknown opcode", opcode)


class Debug:
    def display(self):
        for name, signal in self.__dict__.items():
            if hasattr(signal, "get"):
                print(name, signal.get(), end=' ')
        print("")

if __name__ == "__main__":
    print(hex(get_slice(0x5555, 4, 0)))
    print(hex(get_slice(0xaaaa, 4, 0)))
    print(hex(get_slice(0x5555, 7, 0)))
    print(hex(get_slice(0xaaaa, 7, 0)))
    print(hex(get_slice(0x5555, 7, 4)))
    print(hex(get_slice(0xaaaa, 7, 4)))

    print(sign_extend(0, 3))
    print(sign_extend(1, 3))
    print(sign_extend(2, 3))
    print(sign_extend(3, 3))
    print(sign_extend(4, 3))
    print(sign_extend(5, 3))
    print(sign_extend(6, 3))
    print(sign_extend(7, 3))
