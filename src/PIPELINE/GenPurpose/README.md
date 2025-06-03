# General Purpose Components

This directory contains reusable hardware components used throughout the processor pipeline. These modules provide fundamental operations needed by multiple pipeline stages.
## Modules
# 1. adder.v

Simple adder module for address and data calculations.
## Parameters

    PC_SIZE (default: 32): Data width in bits

## Interface
Signal	Direction	Width	Description
i_A	input	PC_SIZE	First operand
i_B	input	PC_SIZE	Second operand
o_result	output	PC_SIZE	Sum of i_A and i_B
## Features

    Pure combinational logic

    Zero latency

    Used for:

        PC+4 calculation in IF stage

        Branch target calculation in EX stage

        Memory address calculation

# 2. mux2.v

2-to-1 multiplexer with parameterized width.
## Parameters

    PC_SIZE (default: 32): Data width in bits

## Interface
Signal	Direction	Width	Description
i_SEL	input	1	Selection control
i_A	input	PC_SIZE	Input A (selected when SEL=0)
i_B	input	PC_SIZE	Input B (selected when SEL=1)
o_data	output	PC_SIZE	Selected output
## Features

    Used throughout pipeline for:

        ALU source selection

        Register destination selection

        PC source selection

        Memory vs ALU result selection in WB stage

# 3. mux4.v

4-to-1 multiplexer with parameterized width.
## Parameters

    PC_SIZE (default: 32): Data width in bits

    SELECT_SIZE (2): Selection signal width

## Interface
Signal	Direction	Width	Description
i_SEL	input	SELECT_SIZE	Selection control
i_A	input	PC_SIZE	Input A (SEL=00)
i_B	input	PC_SIZE	Input B (SEL=01)
i_C	input	PC_SIZE	Input C (SEL=10)
i_D	input	PC_SIZE	Input D (SEL=11)
o_data	output	PC_SIZE	Selected output
## Features

    Primarily used for:

        Data forwarding in EX stage

        Hazard resolution

        Debug interface selection

# Usage Notes

    All modules are purely combinational

    Default parameter values are optimized for 32-bit architecture

    To instantiate with custom width:
    verilog

    mux2 #(.PC_SIZE(64)) my_mux (...);

    Timing characteristics:

        adder: 1 adder propagation delay

        mux2: 1 mux propagation delay

        mux4: ~1.5x mux2 delay (due to wider selection)

## Typical Applications
Module	Pipeline Usage Examples
adder	PC increment, branch target calculation, address calculation
mux2	ALU source selection, register destination selection, PC source selection
mux4	Data forwarding, hazard resolution, debug interface

### These components form the building blocks for more complex pipeline stages and are designed for maximum reuse across the processor design.