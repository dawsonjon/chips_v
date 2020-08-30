def cpu(instructions, clk, data_in, data_ready):

    #generate a global enable signal
    stall = Boolean().wire()
    global_enable = ~stall

    #simple state machine to control pipeline
    flush = Boolean().wire()
    fetch   = Boolean().constant(1)
    decode  = Boolean().register(clk, en=global_enable, init=0, d=fetch & ~flush)
    execute = Boolean().register(clk, en=global_enable, init=0, d=decode & ~flush)

    ############################################################################# 
    # Fetch - pipeline stage 0
    ############################################################################# 

    pc = Unsigned(32).register(clk, init=0, en=fetch & global_enable)
    instruction = Unsigned(32).rom(pc, *instructions)
    instruction, this_pc = register(clk, fetch & global_enable, instruction, pc)

    ############################################################################# 

                                    ###

    ############################################################################# 
    # Decode - pipeline stage 1
    ############################################################################# 

    #read registers
    decoder_rs1 = instruction[19:15]
    decoder_rs2 = instruction[24:20]
    rd = instruction[11:7]
    registersa = Signed(32).subtype.ram(clk=clk, depth=32)
    registersb = Signed(32).subtype.ram(clk=clk, depth=32)
    src1 = registersa.read(decoder_rs1)
    src2 = registersb.read(decoder_rs2)

    #decode instruction
    fwd1 = Boolean().wire()
    fwd2 = Boolean().wire()
    fwd_val = Signed(32).wire()
    decode_outputs = decode(instruction, src1, src2, fwd1, fwd2, fwd_val, this_pc)
    decode_outputs += (this_pc, rd)

    #register outputs
    decode_outputs = register(clk, global_enable & decode, *decoded_outputs)
    (src1, src2, A, B, operation, shift_amount, add_sub, signed, this_pc, rd) = decode_outputs

    ############################################################################# 

                                    ###

    ############################################################################# 
    # Execute - pipeline stage 2
    ############################################################################# 

    #execute instruction
    execute_outputs = execute(instruction, src1, src2, A, B, operation, add_sub, shift_amount, signed, data_in, this_pc)
    (write_data, write_enable, data_out, address_out, byte_enable, data_valid, take_branch, branch_address) = execute_outputs

    #write registers
    registersa.write(rd, data_out, write_enable & execute & global_enable)
    registersb.write(rd, data_out, write_enable & execute & global_enable)

    #register forwarding
    fwd1.drive(decoder_rs1 == rd & write_enable & execute & global_enable)
    fwd2.drive(decoder_rs2 == rd & write_enable & execute & global_enable)
    fwd_val.drive(data_out)

    ############################################################################# 

    # Increment Program Counter
    pc.d(Unsigned(32).select(take_branch & execute, pc+4, branch_address))
    flush.drive(execute & take_branch)

    #stall the whole pipeline if we are waiting for some event before we continue
    stall.drive(execute & data_valid & ~data_ready) #|go and ~done

    return data_out, address_out, byte_enable, data_valid
