# Pipeline Registers Documentation

These modules serve as intermediate buffers between pipeline stages, ensuring proper synchronization and data forwarding in the processor pipeline.
## Modules Overview
# 1. IF_ID.v

Instruction Fetch to Instruction Decode Buffer
## Parameters
Parameter	Value	Description
PC_SIZE	32	Program counter width
INSTRUCTION_SIZE	32	Instruction width
## Key Features

    Buffers PC+4 value and fetched instruction

    Handles pipeline stalls and flushes:

        - i_enable: Stall control (1 = stall)

        - i_flush: Flush control (1 = flush)

    Synchronized to negative clock edge

    Reset clears all registers

## Interface
Inputs	Outputs
i_adder_result (PC+4)	o_adder_result
i_instruction	o_instruction
# 2. ID_EX.v

Instruction Decode to Execution Buffer
## Parameters
Parameter	Value	Description
ALU_OP_SIZE	6	ALU operation code width
IMM_SIZE	32	Immediate value width
PC_SIZE	32	Program counter width
DATA_SIZE	32	Data bus width
REG_SIZE	5	Register address width
## Key Features

    Buffers all control signals for EX stage

    Preserves register values and immediate data

    Maintains memory access size flags

    Handles jump and halt signals

## Data Paths
Type	Signals
Control	reg_write, mem_to_reg, mem_read, mem_write, branch, alu_src, reg_dest
ALU	alu_op, shamt
Data	data_a, data_b, immediate
Registers	rt, rd, rs
# 3. EX_MEM.v

Execution to Memory Buffer
## Parameters
Parameter	Value	Description
PC_SIZE	32	Program counter width
REG_SIZE	5	Register address width
## Key Features

    Buffers ALU results and memory operands

    Preserves branch resolution information

    Maintains memory control signals

    Handles flush operations from stall unit

    Propagates jump and halt signals

## Critical Signals
Signal	Purpose
alu_result	Memory address or ALU result
data_b	Store data for memory writes
branch_addr	Calculated branch target
zero	Branch condition result
# 4. MEM_WB.v

Memory to Write Back Buffer
## Parameters
Parameter	Value	Description
DATA_SIZE	32	Data bus width
REG_SIZE	5	Register address width
PC_SIZE	32	Program counter width
## Key Features

    Buffers memory read data and ALU results

    Preserves register write control signals

    Handles JAL/JALR special cases

    Propagates halt signal

## Data Selection
Signal	Source
mem_data	Data memory read
alu_result	EX stage result
pc	For JAL/JALR instructions
## Common Characteristics

### Timing:

        All registers update on negative clock edge

        Zero-latency propagation when enabled

### Reset Behavior:

        Synchronous reset clears all registers

        All control signals set to inactive state

### Pipeline Control:

        i_pipeline_enable: Global enable from debug unit

        Stage-specific stall/flush handling

### Data Integrity:

        When stalled, registers maintain current values

        When flushed, control signals are cleared while preserving critical data

## Typical Operation Cycle

### Positive Clock Edge:

        Pipeline stages perform computations

### Negative Clock Edge:

        Pipeline registers capture new values

        Stalled registers maintain state

        Flushed registers clear control signals

### Next Positive Edge:

        Downstream stages use registered values

## Debug Considerations

All pipeline registers include debug unit enable signals (i_pipeline_enable) to allow:

    Pipeline freezing for inspection

    Controlled single-stepping

    Debugger visibility into pipeline state