f unsigned(a):
	return Unsigned(a.subtype.bits).constant(0)+a

def signed(a):
	return Signed(a.subtype.bits).constant(0)+a

def decode(pipeline_in, register_file):

    instruction = pipeline_in.instruction
    this_pc = pipeline_in.instruction

    rs1    = instruction[19:15]
    rs2    = instruction[24:20]
    opcode = instruction[6:0]
    shamt  = instruction[24:20]
    funct3 = instruction[14:12]

    opcode_is_immediate = (opcode == 0b0010011)
    opcode_is_lui       = (opcode == 0b0110111)
    opcode_is_auipc     = (opcode == 0b0010111)
    opcode_is_jal       = (opcode == 0b1101111)
    opcode_is_jalr      = (opcode == 0b1100111)

    #read registers
    src1 = register_file[0].read(rs1)
    src2 = register_file[1].read(rs2)

    #x0 should always read 0
    src1 = Signed(32).select(rs1==0, src1, 0)
    src2 = Signed(32).select(rs2==0, src2, 0)

    #forward result of register that has just been written
    register_forwarding = Struct()
    register_forwarding.forward_1 = Boolean.Wire()
    register_forwarding.forward_2 = Boolean.Wire()
    register_forwarding.forward_data = Signed(32).Wire()
    register_forwarding.rs1 = rs1
    register_forwarding.rs2 = rs2
    src1 = Signed(32).select(forward1, src1, forward_data)
    src2 = Signed(32).select(forward2, src2, forward_data)

    #for register - register instructions use register values for A and B
    A = src1
    B = src2

    #for register - immediate instructions substitute B for an immediate
    B                = Signed(32).select(opcode_is_immediate, src2, Signed(32).constant(0) + inp.instruction[31:20])
    alu_shift_sign   = Signed(1).select(inp.instruction[30], 0, A[31])
    alu_shift_amount = select(opcode_is_immediate, B[4:0], shamt)
    alu_add_sub      = select(opcode_is_immediate, 0, instruction[30])
    alu_operation    = funct3

    #for LUI instructions override ALU inputs
    A           = Signed(32).select(opcode_is_lui,   A, inp.instruction[31:12].resize(32)<<12) #LUI
    B           = Signed(32).select(opcode_is_lui,   B, Signed(32).constant(0))            #LUI
    alu_add_sub = Boolean().select(opcode_is_lui,   0, inp.instruction[30])

    #for AUIPC instructions override ALU inputs
    A           = Signed(32).select(opcode_is_auipc, A, inp.instruction[31:12].resize(32)<<12) #AUIPC
    B           = Signed(32).select(opcode_is_lui,   B, inp.this_pc)                           #AUIPC
    alu_add_sub = Boolean().select(opcode_is_lui,   0, inp.instruction[30])

    #for JAL/JALR instructions override ALU inputs
    A           = Signed(32).select(opcode_is_jal | opcode_is_jalr, A, this_pc+4) #AUIPC
    B           = Signed(32).select(opcode_is_jal | opcode_is_jalr, B, Signed(32).constant(0))            #LUI
    alu_add_sub = Boolean().select(opcode_is_jal | opcode_is_jalr, 0, instruction[30])

    pipeline_out = Struct()
    pipeline_out.instruction = instruction
    pipeline_out.this_pc = this_pc
    pipeline_out.A = A
    pipeline_out.B = B
    pipeline_out.alu_shift_sign
    pipeline_out.alu_shift_amount
    pipeline_out.alu_add_sub
    pipeline_out.alu_operation
    pipeline_out.src1 = src1
    pipeline_out.src2 = src2

    return pipeline_out


def execute(clk, registers_a, registers_b, pipe_in, data_bus):

    #implement ALU
    write_data = select(alu_operation
	    Signed(32).select(add_sub, A+B, A-B)  #ADD/SUB
	    A << alu_shift_amount                 #SLL
        A < B,                        #SLT
        unsigned(A) < unsigned(B),    #SLTU
        A ^ B,                        #XOR
        (sign.cat(A) >> shamt)[31:0], #SRL/SRA
        A | B,                        #OR
        A & B,                        #AND
    )

    #sign extend a portion of the data bus input in load operations
    data_in = Signed(32).select(funct3,
        data_bus.data_in[7:0].resize(32),                   #LB
        data_bus.data_in[15:0].resize(32),                  #LH
        data_bus.data_in[31:0],                             #LW
        Unsigned(32).constant(0)
        Unsigned(32).constant(0) + data_bus.data_in[7:0],   #LBU
        Unsigned(32).constant(0) + data_bus.data_in[15:0],  #LBU
    )
    write_data = select(opcode_is_load,  write_data, data_in) #load instructions
    data_out = src2
    address_offset = select(opcode_is_store, instruction[31:20], instruction[31:20].cat(instruction[11:7])
    address_out = src1 + signed(address_offset)
    byte_enable = select(funct3,
         1 << unsigned(address_bus_out[1:0]), #SB
         3 << unsigned(address_bus_out[0]),   #SH
         15                                   #SW
    )
    stb = execute & (opcode_is_load | opcode_is_store)


    #implement branch instructions
    take_branch.drive(execute & select(funct3,
        src1 == src2,
        src1 != src2,
        0,
        0,
        src1 < src2,
        src1 >= src2,
        unsigned(src1) < unsigned(src2)
        unsigned(src1) >= unsigned(src2)
    ))
    branch_offset = cat(instruction[31], instruction[7], instruction[30:25], instruction[11:6])
    next_pc = select(take_branch, pc + 4, this_pc + branch_offset)

    #implement immediate instructions
    

    #implement program counter

    #register write back
    write = execute
    write |= ~opcode[6]
    write |= opcode_is_jal | opcode_is_jalr #JAL/JALR

    #implement flow control
    enable.drive(~stb | ack)

    #forward result to decode stage



def cpu(clk, instructions, data_in, ack):

    enable        = Boolean().wire()
    take_branch   = Boolean().wire()
    read          = register(clk, en=enable, init=0, d=~take_branch)
    execute       = register(clk, en=enable, init=0, d=read&~take_branch)
    pc            = Signed(32).register(clk, en=enable, init=0)
    registersa    = Signed(32).subtype.ram(clk=clk, depth=32)
    registersb    = Signed(32).subtype.ram(clk=clk, depth=32)

    #fetch
    ######################################################################
    instruction = Signed(32).rom(program_counter, instructions)
    instruction, this_pc = pipeline_register(clk, enable, instruction, pc)

    #decode
    ######################################################################
    pipeline, register_forwarding = decode(pipeline, registersa, registersb)
    pipline = register_pipeline(enable & decode)

    #execute
    ######################################################################
    pipeline = execute(pipeline, register_forwarding)

    #update program counter
    pc.d(pipeline.next_pc)
    registersa.write(pipeline.rd, pipeline.write_data, pipeline.write)
    registersb.write(pipeline.rd, pipeline.write_data, pipeline.write)
