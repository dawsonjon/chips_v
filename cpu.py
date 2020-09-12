from baremetal import *

from decode import decode
from execute import execute
from m_extension import m_extension
from utils import *


def cpu(instruction, clk, bus, march="rv32im"):

    master = bus.add_master()
    debug = Debug()

    # generate a global enable signal
    stall = Boolean().wire()
    global_enable = ~stall

    # simple state machine to control pipeline
    flush = Boolean().wire()
    fetch_en = Boolean().constant(1)
    decode_en = Boolean().register(
        clk, en=global_enable, init=0, d=fetch_en & ~flush)
    execute_en = Boolean().register(
        clk, en=global_enable, init=0, d=decode_en & ~flush)

    #########################################################################
    # Fetch - pipeline stage 0
    #########################################################################

    pc = Unsigned(32).register(clk, init=0, en=fetch_en & global_enable)
    instruction_en = fetch_en & global_enable
    this_pc, = register(clk, instruction_en, pc)
    fetched_instruction = instruction

    #########################################################################
    # Decode - pipeline stage 1
    #########################################################################

    # read registers
    decoder_rs1 = instruction[19:15]
    decoder_rs2 = instruction[24:20]
    registersa = Signed(32).ram(clk=clk, depth=32)
    registersb = Signed(32).ram(clk=clk, depth=32)
    src1 = registersa.read(decoder_rs1)
    src2 = registersb.read(decoder_rs2)

    # decode instruction
    fwd1 = Boolean().wire()
    fwd2 = Boolean().wire()
    fwd_val = Signed(32).wire()
    decode_outputs = decode(
        instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc)
    decode_outputs += (instruction, this_pc)

    # register outputs
    decode_outputs = register(clk, global_enable & decode_en, *decode_outputs)
    (src1, src2, A, B, operation, shift_amount, add_sub, signed,
     instruction, this_pc) = decode_outputs

    #########################################################################
    # Execute - pipeline stage 2
    #########################################################################

    # execute instruction
    execute_outputs = execute(
        instruction, src1, src2, A, B, operation, add_sub, shift_amount,
        signed, master.s2m, this_pc)
    (write_data, write_enable, data_out, address, byte_enable,
        data_valid, write_read, take_branch,
        branch_address) = execute_outputs

    master.address.drive(address)
    master.m2s.drive(data_out)
    master.byte_enable.drive(byte_enable)
    master.write_read.drive(write_read)
    master.valid.drive(data_valid)

    # optionally enable multiply/divide/modulo logic for m extension
    if "m" in march:
        (
            m_write_data,
            m_write_enable,
            m_wait
        ) = m_extension(clk, A, B, instruction)
        write_data = write_data.subtype.select(
            m_write_enable, write_data, m_write_data)
        write_enable = write_enable | m_write_enable
        debug.m_write_data = m_write_data
        debug.m_write_enable = m_write_enable
        debug.m_wait = m_wait
    else:
        m_wait = Boolean().constant(0)

    # write registers
    rd = instruction[11:7]
    registersa.write(
        rd, write_data, write_enable & execute_en & global_enable)
    registersb.write(
        rd, write_data, write_enable & execute_en & global_enable)

    # register forwarding
    fwd1.drive(
        (decoder_rs1 == rd) & write_enable & execute_en & global_enable)
    fwd2.drive(
        (decoder_rs2 == rd) & write_enable & execute_en & global_enable)
    fwd_val.drive(write_data)

    #########################################################################

    # Increment Program Counter
    pc.d(Unsigned(32).select(
        take_branch & execute_en, pc + 4, branch_address))
    flush.drive(execute_en & take_branch)

    # stall the whole pipeline if we are waiting for some event before we
    # continue
    stall.drive(execute_en & ((master.valid & ~master.ready) | m_wait))

    debug.fetch_en = fetch_en
    debug.decode_en = decode_en
    debug.execute_en = execute_en
    debug.this_pc = this_pc
    debug.fetched_instruction = fetched_instruction
    debug.instruction = instruction
    debug.flush = flush
    debug.stall = stall
    debug.take_branch = take_branch
    debug.src1 = src1
    debug.src2 = src2
    debug.fwd1 = fwd1
    debug.fwd2 = fwd2
    debug.fwd_val = fwd_val
    debug.write_data = write_data
    debug.write_enable = write_enable
    debug.rd = rd
    debug.global_enable = global_enable
    debug.branch_address = branch_address
    debug.pc = pc
    debug.rd = rd
    debug.decoder_rs1 = decoder_rs1
    debug.decoder_rs2 = decoder_rs2

    return pc, instruction_en, debug
