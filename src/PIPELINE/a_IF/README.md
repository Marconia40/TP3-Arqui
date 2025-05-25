# Instruction Fetch (IF) Stage - Pipeline Documentation
## Overview

The Instruction Fetch (IF) stage is the first phase of the processor pipeline. This module is responsible for fetching instructions from instruction memory and preparing them for decoding in the next pipeline stage. It also determines the address of the next instruction to be executed.
## Module Components
# 1. IFETCH (Top-Level Module)

The main module that coordinates all components of the instruction fetch stage.
## Parameters

    PC_SIZE (default: 32): Size of the program counter in bits

    INSTRUCTION_SIZE (default: 32): Size of instructions in bits

    INSTMEM_SIZE (default: 8): Size of instruction memory address bus

    MEM_SIZE (default: 8): Size of memory data bus

## Inputs

### Clock and Control Signals:

        i_clock: System clock signal

        i_pc_enable: Enables the program counter

        i_pc_reset: Resets the program counter to zero

        i_pc_stall: Stalls the PC when active (1 = stall, 0 = normal operation)

### Memory Control Signals:

        i_read_enable: Enables instruction memory read operations

        i_instru_mem_enable: Enables the instruction memory

        i_write_enable: Enables instruction memory writes (for debug purposes)

        i_write_data: Data to write to instruction memory (debug)

        i_write_addr: Address for instruction memory writes (debug)

### Branch/Jump Control:

        i_branch: Indicates a branch instruction (1 = branch, 0 = no branch)

        i_j_jal: Indicates a jump instruction (J or JAL)

        i_jr_jalr: Indicates a jump register instruction (JR or JALR)

### Target Addresses:

        i_branch_addr: Branch target address

        i_jump_addr: Jump target address (for J and JAL)

        i_data_last_register: Jump target address (for JR and JALR)

## Outputs

    o_last_pc: Current program counter value

    o_adder_result: Next sequential PC value (PC + 4)

    o_instruction: Fetched instruction from memory

## Functionality

The IFETCH module coordinates all components of the instruction fetch stage:

    Manages the program counter to track instruction addresses

    Handles branch and jump target selection through multiplexers

    Interfaces with instruction memory to fetch instructions

    Calculates the next sequential address (PC + 4)

    Provides stall capability for pipeline control

# 2. program_counter.v

Maintains and updates the program counter value.
## Parameters

    PC_SIZE (default: 32): Size of the program counter in bits

## Inputs

    i_enable: Module enable signal

    i_clock: System clock

    i_reset: Resets PC to zero when active

    i_mux_pc: Next PC value from multiplexer

    i_pc_stall: When 1, PC maintains current value; when 0, updates normally

## Outputs

    o_pc: Current program counter value

## Functionality

    Updates the PC value on each clock cycle when enabled

    Can be reset to zero

    Supports stalling to maintain current PC value

    Outputs current PC value to instruction memory and adder

# 3. inst_mem.v

Instruction memory module that stores and provides program instructions.
## Parameters

    MEM_SIZE (default: 8): Size of memory data bus

    ENTRIES_SIZE (default: 256): Depth of instruction memory (number of entries)

    DIR_ADDR_SIZE (default: 8): Size of address bus for writes

    ADDR_SIZE (default: 32): Size of address bus for reads

    INSTRUCTION_SIZE (default: 32): Size of instructions in bits

## Inputs

    i_clock: System clock

    i_enable: Memory enable signal

    i_read_enable: Enables read operations

    i_write_enable: Enables write operations (for debug)

    i_write_data: Data to write to memory (debug)

    i_write_addr: Write address (debug)

    i_read_addr: Read address (from PC)

## Outputs

    o_read_data: Fetched instruction (32 bits)

## Functionality

    Stores program instructions in a block RAM (BRAM)

    Reads 32-bit instructions by combining four 8-bit memory locations

    Supports debug writes to memory when enabled

    Outputs the instruction at the current PC address

# 4. latch.v

Pipeline register that holds the next PC value between stages.
## Parameters

    PC_SIZE (default: 32): Size of the PC value in bits

## Inputs

    i_clock: System clock

    i_next_pc: Next PC value to store

## Outputs

    o_next_pc: Registered output of next PC value

## Functionality

    Simple register that captures the next PC value (PC + 4) on clock edges

    Helps maintain pipeline timing by registering signals between stages

## Data Flow

    The program counter provides the current instruction address

    The instruction memory returns the instruction at that address

    An adder calculates PC + 4 (next sequential address)

    Multiplexers select between:

        Sequential address (PC + 4)

        Branch target address

        Jump target address

        Register-based jump address

    The selected address becomes the next PC value

    The current PC and instruction are passed to the next pipeline stage

## Control Flow

The module supports several control flow operations:

    Sequential execution: PC increments by 4 each cycle

    Branches: PC updates to branch target when taken

    Jumps: PC updates to absolute jump address

    Jump registers: PC updates to address from register file

    Stalls: PC maintains current value when pipeline is stalled