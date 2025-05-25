# Instruction Decode (ID) Stage - Pipeline Documentation
## Overview

The Instruction Decode stage is responsible for decoding instructions fetched from memory, reading register values, and generating control signals for subsequent pipeline stages.
## Module Components
# 1. IDECODE (Top-Level Module)

The main module that coordinates all components of the instruction decode stage.
## Parameters

    INSTRUCTION_SIZE (32): Instruction width in bits

    PC_SIZE (32): Program counter width

    DATA_SIZE (32): Data bus width

    REG_SIZE (5): Register address width

    ALU_OP_SIZE (6): ALU operation code width

## Inputs

### Clock and Control:

        i_clock: System clock

        i_pipeline_enable: Pipeline enable signal

        i_reset: Reset signal

        i_flush_unit_ctrl: Flush control signals (from hazard unit)

### Debug Interface:

        i_unit_control_enable: Enables control unit

        i_rb_enable: Enables register bank

        i_rb_read_enable: Enables register bank read

        i_rb_read_addr: Register read address for debug

### Pipeline Inputs:

        i_inst: Instruction from fetch stage

        i_pc: Program counter value from fetch stage

        i_write_data: Data to write to register file (from WB stage)

        i_write_reg: Register write address (from WB stage)

        i_reg_write: Register write enable (from WB stage)

## Outputs

### Control Signals:

        o_signed: Signed operation flag

        o_reg_dest: Register destination select

        o_alu_op: ALU operation code

        o_alu_src: ALU source select

        o_mem_read: Memory read enable

        o_mem_write: Memory write enable

        o_branch: Branch instruction flag

        o_reg_write: Register write enable

        o_mem_to_reg: Memory to register select

        o_jump: Jump instruction flag

        o_jr_jalr: Jump register instruction flag

        o_halt: Processor halt signal

        Memory access size flags (o_byte_enable, o_halfword_enable, o_word_enable)

### Data Outputs:

        o_data_a, o_data_b: Register read values

        o_immediate: Sign-extended immediate value

        o_shamt: Shift amount

        o_jump_addr: Calculated jump address

        Register addresses (o_rt, o_rd, o_rs)

        o_pc: Pass-through PC value

# 2. bank_register.v

The register file containing 32 general-purpose registers.
## Parameters

    DATA_SIZE (32): Data width

    REG_SIZE (5): Register address width

    BANK_SIZE (32): Number of registers

## Features

    Dual read ports, single write port

    Handles RAW hazards by forwarding written data

    Debug interface for external access

    Reset capability

# 3. unit_control.v

The main control unit that decodes instructions and generates control signals.
## Features

    Decodes both opcode and function fields for R-type instructions

    Generates control signals for all pipeline stages

    Handles flush signals from hazard unit

    Supports all MIPS instruction types including:

        Arithmetic/logical operations

        Memory access (load/store)

        Branches and jumps

        System operations (halt)

# 4. sign_extend.v

Sign-extends 16-bit immediate values to 32 bits.
# 5. expand.v

Zero-extends 5-bit values (like shift amounts) to 32 bits.
# 6. jump_addr.v

Calculates jump addresses for J-type instructions by combining:

    Upper 4 bits of PC+4

    26-bit immediate from instruction

    2 zero bits

## Data Flow
 
    Instruction arrives from IF stage

    Control unit decodes opcode/function bits

    Register file reads two source registers

    Immediate value is sign-extended

    Jump address is calculated (if needed)

    All outputs are registered for next pipeline stage