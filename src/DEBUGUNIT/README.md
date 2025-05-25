# Debug Unit Documentation
## Overview

The debug unit module provides comprehensive debugging capabilities for the MIPS pipeline processor through a UART interface. It allows for processor control, memory inspection, and register file access during operation.
## Key Features

### UART Communication Interface:

-        Receives commands via RX

-       Transmits data via TX

-        Handles byte-level communication

### Processor Control:

-        Start/stop execution

-        Single-step operation

-        Pipeline enable/disable

### Memory Access:

-        Instruction memory writes

-        Data memory reads

-        Byte-level memory inspection

### Register Inspection:

-        Full register file access

-        32-bit register value reading

### Status Monitoring:

-        Program counter inspection

-        Processor halt detection

## Interface
### Inputs
Signal	Width	Description
i_clock	1	System clock
i_reset	1	Active-high reset
i_halt	1	Processor halt status
i_rx_done	1	UART RX byte ready
i_tx_done	1	UART TX byte sent
i_rx_data	8	Received UART data
i_pc_value	32	Current PC value
i_mem_data	32	Data memory contents
i_bank_reg_data	32	Register file data
### Outputs
Signal	Width	Description
o_instru_mem_data	8	Instruction memory write data
o_instru_mem_addr	8	Instruction memory address
o_rb_addr	5	Register file read address
o_mem_data_addr	5	Data memory read address
o_tx_data	8	UART transmit data
o_tx_start	1	UART transmit start
o_instru_mem_write_enable	1	Instruction memory write enable
o_instru_mem_read_enable	1	Instruction memory read enable
o_instru_mem_enable	1	Instruction memory enable
o_rb_read_enable	1	Register file read enable
o_rb_enable	1	Register file enable
o_mem_data_enable	1	Data memory enable
o_mem_data_read_enable	1	Data memory read enable
o_mem_data_debug_unit	1	Data memory debug access
o_unit_control_enable	1	Control unit enable
o_pc_enable	1	Program counter enable
o_state	10	Current debug state
o_pipeline_enable	1	Pipeline enable
## Command Set

The debug unit responds to the following UART commands:
Command	Value	Description
CMD_WRITE_IM	0x01	Write to instruction memory
CMD_SEND_INFO	0x02	Request processor state
CMD_STEP_BY_STEP	0x03	Enter single-step mode
CMD_CONTINUE	0x04	Resume continuous execution
CMD_STEP	0x05	Execute single instruction
## State Machine

The debug unit operates through these states:

### INITIAL:

-        Waits for initial command

-        Disables all processor components

### WRITE_IM:

-        Handles instruction memory programming

-        Writes sequential bytes from UART

### READY:

-        Waits for execution command

-        Ready for step/continue operations

### START:

-        Continuous execution mode

-        Monitors for halt condition

### STEP_BY_STEP:

-        Single-step execution mode

-        Requires step command for each instruction

### SEND_PC:

-        Transmits PC value via UART

-        Sends 4 bytes (MSB first)

### SEND_MEM:

-        Transmits data memory contents

-        Scans entire memory space

### SEND_BR:

-        Transmits register file contents

-        Scans all 32 registers

## Operation Modes
### Programming Mode

    Activated by CMD_WRITE_IM

    Loads instruction memory via UART

    Sequential byte writes

    Automatic address increment

### Inspection Mode

    Activated by CMD_SEND_INFO

    Transmits:

        Current PC value

        Data memory contents

        Register file contents

    Big-endian byte order

### Execution Control

    Continuous mode: Free-running execution

    Single-step mode: Manual instruction advance

    Automatic halt detection

## Timing Characteristics

    Synchronous to system clock

    UART operations are byte-oriented

    State transitions occur on clock edges

    All control signals are registered

## Usage Example

    Reset processor

    Send CMD_WRITE_IM to enter programming mode

    Send instruction bytes (256 max)

    Send CMD_STEP_BY_STEP for single-step debugging

    Send CMD_STEP to execute each instruction

    Send CMD_SEND_INFO to inspect state

## Error Handling

    Automatic state reset on system reset

    Byte counters reset after complete transfers

    Safe defaults for all control signals