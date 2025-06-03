# Memory (MEM) Stage - Pipeline Documentation
## Overview

The Memory stage handles all data memory operations, including load/store instructions and branch resolution. It also manages the interface between the processor pipeline and debug units.
## Module Components
# 1. MEMORY (Top-Level Module)

Coordinates all memory stage components.
## Parameters

    ADDR_SIZE (32): Memory address width

    DATA_SIZE (32): Data bus width

    PC_SIZE (32): Program counter width

    REG_SIZE (5): Register address width

    BANK_SIZE (32): Memory depth (32 words)

## Inputs

### Clock and Control:

        i_clock: System clock

        i_debug_unit_flag: Debug mode enable

        i_memory_data_enable: Memory enable (debug)

        i_memory_data_read_enable: Memory read enable (debug)

        i_memory_data_read_addr: Memory read address (debug)

### Pipeline Control Signals:

        i_signed: Signed operation flag

        i_reg_write: Register write enable (WB stage)

        i_mem_to_reg: Memory to register select (WB stage)

        i_mem_read: Memory read enable

        i_mem_write: Memory write enable

        Memory size flags (i_complete_word, i_halfword_enable, i_byte_enable)

        i_branch: Branch instruction flag

        i_zero: ALU zero flag

        i_last_register_ctrl: Special register control

        i_halt: Processor halt signal

### Data Inputs:

        i_branch_addr: Branch target address

        i_alu_result: ALU result (memory address)

        i_write_data: Data to write to memory

        i_selected_reg: Destination register address

        i_pc: Program counter value

## Outputs

### Memory Interface:

        o_mem_data: Memory read data (to register file)

        o_read_dm: Memory read data (to debug unit)

### Pipeline Control:

        o_branch_zero: Branch condition result

        o_reg_write: Register write enable (to WB)

        o_mem_to_reg: Memory to register select (to WB)

        o_last_register_ctrl: Special register control (to WB)

        o_halt: Processor halt signal (to WB)

### Data Outputs:

        o_selected_reg: Destination register (to WB)

        o_alu_result: ALU result (to WB)

        o_branch_addr: Branch target address (to IF)

        o_pc: Program counter value (to WB)

# 2. mem_data.v

Data memory storage (32x32 RAM).
## Features:

    Synchronous read/write operations

    Single read/write port

    32-word capacity (32-bit words)

    Debug interface support

    Initializes all memory locations to zero

# 3. mem_ctrl.v

Memory access controller.
## Parameters:

    DATA_SIZE (32): Data width

    TYPE_SIZE (3): Memory access type width

## Functions:

### Handles sign extension for load operations:

        Byte (8-bit)

        Halfword (16-bit)

        Word (32-bit)

### Manages write data sizing:

        Truncates data for byte/halfword writes

### Memory access type encoding:

        BYTE_WORD: 8-bit access

        HALF_WORD: 16-bit access

        COMPLETE_WORD: 32-bit access

# 4. select.v

Memory access selector.
## Functions:

    Multiplexes between normal pipeline operation and debug access

    Prevents debug writes to memory (read-only in debug mode)

    Selects address source:

        Pipeline: ALU result (normal operation)

        Debug unit: Debug address (debug mode)

## Data Flow

    Receives memory address from EX stage (ALU result)

    Selects between pipeline/debug modes

    Performs memory access:

        Reads: Handles sign extension and sizing

        Writes: Truncates data to appropriate size

    Resolves branch conditions

    Passes control signals and data to WB stage

## Key Features

    Flexible Memory Access: Supports 8/16/32-bit accesses

    Sign Handling: Properly extends signed/unsigned values

    Debug Interface: Allows memory inspection without disrupting pipeline

    Memory Protection: Debug mode is read-only

    Branch Resolution: Combines branch signal and zero flag for IF stage

## Memory Access Types
Signal Combination	Access Type	Size
i_complete_word = 1	Word	32-bit
i_halfword_enable = 1	Halfword	16-bit
i_byte_enable = 1	Byte	8-bit
Debug Interface

### When i_debug_unit_flag is active:

    Memory reads use debug unit address

    Memory writes are disabled

    Normal pipeline memory operations are suspended

    Read data available on o_read_dm