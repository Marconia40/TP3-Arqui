# Write Back (WB) Stage - Pipeline Documentation
## Overview

The Write Back stage is the final stage of the processor pipeline, responsible for writing computation results back to the register file. It selects between memory data and ALU results, and handles special cases like jump-and-link instructions.
## Module Components
# WBACK (Write Back Module)
## Parameters
Parameter	Value	Description
DATA_SIZE	32	Data bus width in bits
REG_SIZE	5	Register address width in bits
PC_SIZE	32	Program counter width in bits
## Inputs

### Control Signals:

        i_reg_write: Register write enable signal

        i_mem_to_reg: Selects between memory data and ALU result

        i_last_register_ctrl: Special control for JAL/JALR instructions

        i_halt: Processor halt signal

### Data Inputs:

        i_mem_data: Data read from memory (for load instructions)

        i_alu_result: Result from ALU (for R-type and store instructions)

        i_selected_reg: Destination register address

        i_pc: Program counter value (for JAL/JALR)

## Outputs
Output	Description
o_reg_write	Register write enable signal to register file
o_selected_data	Data to be written to register file (selected through multiplexers)
o_selected_reg	Destination register address
o_halt	Processor halt signal
## Data Flow

### First Multiplexer (Memory vs ALU):

####    Selects between:

            i_alu_result (for R-type and store instructions)

            i_mem_data (for load instructions)

####    Controlled by i_mem_to_reg signal

### Second Multiplexer (Normal vs PC Value):

####    Selects between:

            Output from first mux (normal operation)

            i_pc value (for JAL/JALR instructions)

####    Controlled by i_last_register_ctrl signal

## Output Stage:

        Passes selected data to register file

        Preserves register write enable signal

        Passes through destination register address

        Propagates halt signal

## Key Features

### Flexible Data Selection:

        Handles both memory loads and ALU results

        Supports special cases like JAL/JALR

### Pipeline Integration:

        Preserves all control signals

        Maintains data integrity

### Simple Design:

        Pure combinational logic (no clock dependency)

        Minimal propagation delay

## Special Cases

### Jump-and-Link Instructions:

        When i_last_register_ctrl is high, writes PC+4 to register 31

        Used by JAL and JALR instructions to save return address

### Memory Loads:

        When i_mem_to_reg is high, writes memory data to destination register

        Used by LB/LH/LW/LBU/LHU instructions

### ALU Operations:

        When i_mem_to_reg is low, writes ALU result to destination register

        Used by all R-type and immediate instructions

## Timing Characteristics

    Zero-cycle latency (combinational)

    Outputs stabilize after multiplexer propagation delay

    No clocked elements in critical path

### This stage completes the processor pipeline by ensuring computation results are properly written back to the register file, maintaining architectural state for subsequent instructions.