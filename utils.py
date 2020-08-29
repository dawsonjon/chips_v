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

if __name__ == "__main__":
    print hex(get_slice(0x5555, 4, 0))
    print hex(get_slice(0xaaaa, 4, 0))
    print hex(get_slice(0x5555, 7, 0))
    print hex(get_slice(0xaaaa, 7, 0))
    print hex(get_slice(0x5555, 7, 4))
    print hex(get_slice(0xaaaa, 7, 4))

    print sign_extend(0, 3)
    print sign_extend(1, 3)
    print sign_extend(2, 3)
    print sign_extend(3, 3)
    print sign_extend(4, 3)
    print sign_extend(5, 3)
    print sign_extend(6, 3)
    print sign_extend(7, 3)
