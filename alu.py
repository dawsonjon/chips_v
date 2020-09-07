from baremetal import *
from utils import *

def alu(A, B, operation, add_sub, shift_amount, is_signed):
    sign   = Signed(1).select(is_signed, 0, A[31])
    shift_amount = signed(shift_amount.resize(6))


    #implement ALU
    write_data = Signed(32).select(operation, 
	    Signed(32).select(add_sub, A+B, A-B),  #000 ADD/SUB
	    A << shift_amount,                     #001 SLL
        (A < B).resize(2),                     #010 SLT
        (unsigned(A) < unsigned(B)).resize(2), #011 SLTU
        A ^ B,                                 #100 XOR
        (sign.cat(A) >> shift_amount)[31:0],   #101 SRL/SRA
        A | B,                                 #110 OR
        A & B,                                 #111 AND
    )

    return write_data

def ALU_model(A, B, operation, add_sub, shift_amount, is_signed):
    A = int32trunc(A)
    B = int32trunc(B)
    if operation == 0:
        if add_sub:
            return int32trunc(A - B)
        else:
            return int32trunc(A + B)
    elif operation == 1:
        return int32trunc(A << shift_amount)
    elif operation == 2:
        return int32trunc(A < B)
    elif operation == 3:
        A = A & 0xffffffff
        B = B & 0xffffffff
        return int32trunc(A < B)
    elif operation == 4:
        return int32trunc(A ^ B)
    elif operation == 5:
        if is_signed:
            return int32trunc(A >> shift_amount)
        else:
            A = A & 0xffffffff
            return int32trunc(A >> shift_amount)
    elif operation == 6:
        return int32trunc(A | B)
    elif operation == 7:
        return int32trunc(A & B)


if __name__ == "__main__":

    import itertools, sys, random

    A = Signed(32).input("A")
    B = Signed(32).input("B")
    operation = Signed(3).input("operation")
    add_sub = Boolean().input("add_sub")
    shift_amount = Unsigned(5).input("shift_amount")
    is_signed = Boolean().input("signed")
    inputs = [A, B, operation, add_sub, shift_amount, is_signed]

    write_data = alu(A, B, operation, add_sub, shift_amount, is_signed)


    A_stim = [0x00000000, 0x00000001, 0x7ffffffe, 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff]
    B_stim = A_stim
    add_sub_stim = [0, 1]
    operation_stim = list(range(8))
    shift_amount_stim = [0b00000, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11110, 0b11111]
    is_signed_stim = [0, 1]


    stimulus = itertools.product(A_stim, B_stim, operation_stim, add_sub_stim, shift_amount_stim, is_signed_stim)
    stimulus = list(stimulus)
    random.shuffle(stimulus)
    for idx, stim in enumerate(stimulus):
        if idx%1000==0:
            print "testing alu", 100*idx/len(stimulus), "%"

        for i, v in zip(inputs, stim):
            i.set(v)
        actual = write_data.get()
        expected = ALU_model(*stim)

        if actual != expected:
            print "fail"
            print "A", int32trunc(stim[0])
            print "B", int32trunc(stim[1])
            print "operation", stim[2]
            print "add_sub", stim[3]
            print "shift_amount", stim[4]
            print "is_signed", stim[5]
            print actual
            print expected
            sys.exit(0)
    print "pass"

