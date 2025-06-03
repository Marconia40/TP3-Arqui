# Execution (EX) Stage - Pipeline Documentation
## Overview
The Execution stage performs all arithmetic and logical operations, calculates memory addresses, resolves branches, and handles data forwarding to resolve hazards.
## Module Components
# 1. EXECUTE (Top-Level Module)

Coordinates all execution stage components.
## Parameters

-    ALU_OP_SIZE (6): ALU operation code width

-    ALU_CTRL_SIZE (4): ALU control signal width

-    IMM_SIZE (32): Immediate value width

-    PC_SIZE (32): Program counter width

-    DATA_SIZE (32): Data bus width

-    REG_SIZE (5): Register address width

-    FUNCTION_SIZE (6): Function code width

-    SELECT_SIZE (2): Forwarding mux select width

## Inputs

### Control Signals from ID:

        i_signed: Signed operation flag

        i_reg_write: Register write enable (WB stage)

        i_mem_to_reg: Memory to register select (WB stage)

        i_mem_read: Memory read enable (MEM stage)

        i_mem_write: Memory write enable (MEM stage)

        i_branch: Branch instruction flag

        i_alu_src: ALU source select (immediate vs register)

        i_reg_dest: Register destination select (rt vs rd)

        i_alu_op: ALU operation code

        Memory access size flags (i_byte_enable, i_halfword_enable, i_word_enable)

        i_halt: Processor halt signal

        i_jump: Jump instruction flag

### Data Inputs:

        i_pc: Program counter value

        i_data_a, i_data_b: Register values

        i_immediate: Sign-extended immediate value

        i_shamt: Shift amount

        i_rt, i_rd: Register addresses

### Forwarding Inputs:

        i_mem_fwd_data: Data from MEM stage for forwarding

        i_wb_fwd_data: Data from WB stage for forwarding

        i_fwd_a: Forwarding select for operand A

        i_fwd_b: Forwarding select for operand B

        i_forwarding_mux: Forwarding select for memory data

## Outputs

### Control Signals to MEM:

        o_signed: Signed operation flag

        o_reg_write: Register write enable

        o_mem_to_reg: Memory to register select

        o_mem_read: Memory read enable

        o_mem_write: Memory write enable

        o_branch: Branch instruction flag

        Memory access size flags (o_byte_enable, o_halfword_enable, o_word_enable)

        o_halt: Processor halt signal

        o_jump: Jump instruction flag

### Data Outputs:

        o_branch_addr: Calculated branch target address

        o_zero: ALU zero flag (for branches)

        o_alu_result: ALU computation result

        o_data_b: Data for memory store operations

        o_selected_reg: Destination register address

        o_last_register_ctrl: Special register select for JALR

        o_pc: Pass-through PC value

# 2. alu.v

## Arithmetic Logic Unit that performs all computations.
### Parameters

    DATA_SIZE (32): Data width

    ALU_CTRL_SIZE (4): Control signal width

## Supported Operations:
Control	Operation	Description
4'h0	SLL/SLLV	Logical left shift
4'h1	SRL/SRLV	Logical right shift
4'h2	SRA/SRAV	Arithmetic right shift
4'h3	ADD/ADDI/ADDU	Addition
4'h4	SUB/SUBI/SUBU	Subtraction
4'h5	AND/ANDI	Bitwise AND
4'h6	OR/ORI	Bitwise OR
4'h7	XOR/XORI	Bitwise XOR
4'h8	NOR	Bitwise NOR
4'h9	SLT/SLTI	Set less than (signed)
4'ha	SLL16	Shift left 16 (for LUI)
4'hb	BEQ	Branch equal comparison
4'hc	BNE	Branch not equal comparison

## Additional Features:

    o_zero: Outputs 1 when result is zero (used for branches)

# 3. alu_ctr.v

Decodes ALU operation from instruction fields.
## Parameters

    FUNCTION_SIZE (6): Function code width

    ALU_OP_SIZE (6): Opcode width

    ALU_CTRL_SIZE (4): ALU control output width

## Functionality:

    Decodes R-type instructions using function field

    Decodes I-type instructions using opcode

    Generates:

        ALU control signals

        Shift amount select (shamt vs register)

        Last register control (for JALR)

# 4. left_shift.v

Left shifts immediate values by 2 for branch address calculation.
## Data Flow

    Receives operands and control signals from ID stage

    Selects between register data and forwarded data using forwarding muxes

    Performs ALU operation based on control signals

    Calculates branch target address (PC + (imm<<2))

    Selects destination register (rt/rd/last_register)

    Passes results and control signals to MEM stage

## Key Features

    Forwarding Support: Handles RAW hazards by forwarding results from:

        EX/MEM pipeline register

        MEM/WB pipeline register

    Branch Resolution: Calculates target addresses and sets zero flag

    Flexible ALU: Supports all MIPS arithmetic/logical operations

    Register Selection: Handles different destination registers for:

        R-type (rd)

        I-type (rt)

        JALR (last_register)