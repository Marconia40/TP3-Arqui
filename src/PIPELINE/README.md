# MIPS Pipeline Processor Documentation
## Overview

This is a 5-stage pipelined MIPS processor implementation with full hazard detection and resolution. The pipeline consists of:

- Instruction Fetch (IF)

- Instruction Decode (ID)

- Execution (EX)

- Memory Access (MEM)

- Write Back (WB)

## Key Features

-   Full Pipeline Implementation: All 5 classic MIPS pipeline stages

-   Hazard Handling:

        Data forwarding (EX/MEM and MEM/WB stages)

        Load-use stalls

        Branch/Jump flushing

-   Memory System:

        Separate instruction and data memories

        Byte/halfword/word addressable data memory

-   Debug Support:

        Memory inspection

        Register file access

        Pipeline control

## Pipeline Stages
### 1. Instruction Fetch (IF)

-   Fetches instructions from instruction memory

-   Handles PC updates and branch/jump targets

-   Modules: IFETCH.v, inst_mem.v, program_counter.v

### 2. Instruction Decode (ID)

-   Decodes instructions and reads register file

-   Generates control signals

-   Sign-extends immediate values

-   Modules: IDECODE.v, bank_register.v, unit_control.v, sign_extend.v

### 3. Execution (EX)

-   Performs ALU operations

-   Calculates branch targets

-   Handles data forwarding

-   Modules: EXECUTE.v, alu.v, alu_ctr.v, forwarding_unit.v

### 4. Memory Access (MEM)

-   Handles load/store operations

-   Manages data memory access

-   Resolves branches

-   Modules: MEMORY.v, mem_data.v, mem_ctrl.v

### 5. Write Back (WB)

-   Writes results back to register file

-   Selects between memory and ALU results

-   Modules: WBACK.v

## Pipeline Registers
Register	Description
IF_ID	Buffers IF stage outputs for ID stage
ID_EX	Buffers ID stage outputs for EX stage
EX_MEM	Buffers EX stage outputs for MEM stage
MEM_WB	Buffers MEM stage outputs for WB stage
## Hazard Handling
### Forwarding Unit

    Resolves RAW hazards by forwarding:

        EX/MEM results to EX inputs

        MEM/WB results to EX inputs

    Handles special cases for store instructions

### Stall Unit

    Detects and handles:

        Load-use hazards (inserts bubbles)

        Branch/jump hazards (flushes pipeline)

        HALT instruction propagation

## Memory System
### Instruction Memory

    256-entry, 8-bit wide memory

    Reads 32-bit instructions in single cycle

    Supports debug writes

### Data Memory

    32-entry, 32-bit wide memory

    Supports byte, halfword and word accesses

    Handles signed/unsigned loads

## Control Signals

Signal propagation through pipeline stages:
Signal	Description	Stages Active
reg_write	Register file write enable	ID, EX, MEM, WB
mem_to_reg	Memory vs ALU result selection	ID, EX, MEM, WB
mem_read	Memory read enable	ID, EX, MEM
mem_write	Memory write enable	ID, EX, MEM
branch	Branch instruction	ID, EX, MEM
alu_src	ALU source (register vs immediate)	ID, EX
reg_dest	Register destination (rt vs rd)	ID, EX
## Debug Interface

The processor supports debug access through:

    Instruction memory inspection/writes

    Data memory reads

    Register file reads

    Pipeline control (enable/disable)

    Current PC value inspection

## Timing Characteristics

    All pipeline stages synchronized to positive clock edge

    Pipeline registers update on negative clock edge

    Critical path through ALU in EX stage

## Parameters

Key configurable parameters:
Parameter	Default	Description
PC_SIZE	32	Program counter width
DATA_SIZE	32	Data bus width
REG_SIZE	5	Register address width
ALU_OP_SIZE	6	ALU operation code width
## Instruction Support

The processor supports:

-   Arithmetic/logical operations

-   Load/store instructions

-   Branches and jumps

-   System operations (HALT)

-   Immediate instructions

## Top-Level Module

The PIPELINE.v module integrates all pipeline stages and hazard detection units, providing:

-   Clock and reset inputs

-   Debug interfaces

-   Pipeline control signals

-   Processor status outputs