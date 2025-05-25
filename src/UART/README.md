# UART Module
## Overview

This repository contains a UART (Universal Asynchronous Receiver-Transmitter) implementation in Verilog. The UART supports configurable data bits and baud rate, with a default configuration of 8 data bits and 19200 baud rate.
## Module Structure

The UART system consists of three main components integrated into a top-level module:

-   Baud Rate Generator (baudrate_gen.v)

        Generates a clock tick signal (s_tick) at 16 times the baud rate (oversampling)

        Configurable clock frequency and baud rate via parameters

        Default: 50 MHz system clock, 19200 baud rate

-   Receiver (rx_uart.v)

        Implements a UART receiver with state machine (IDLE, START, DATA, STOP)

        Samples input data at 16x the baud rate for reliable detection

        Outputs received data with a done tick signal

-   Transmitter (tx_uart.v)

        Implements a UART transmitter with state machine (IDLE, START, DATA, STOP)

        Transmits data at the configured baud rate

        Outputs a done tick signal when transmission completes

## Top-Level Module (UART.v)

-   Integrates all components

-   Provides clean interface with:

        Clock and reset inputs

        RX and TX data lines

        Control signals (transmit start)

        Status signals (receive/transmit done)

## Parameters

    DATA_BITS: Number of data bits (default: 8)

    CLK: System clock frequency (default in baudrate_gen: 50E6)

    BAUDRATE: Communication speed (default: 19200)

    TICKS: Oversampling rate (fixed at 16)

## Signals
### Inputs

-    i_clock: System clock

-    i_reset: Active-high reset

-    i_rx: Serial receive line

-    i_tx_data: Parallel data to transmit

-    i_tx_start: Signal to start transmission

### Outputs

-    o_rx_data: Received parallel data

-    o_rx_done_tick: Pulse when receive completes

-    o_tx: Serial transmit line

-    o_tx_done_tick: Pulse when transmit completes

## Usage

    Instantiate the UART module in your design

    Connect clock and reset signals

    For receiving:

        Monitor o_rx_done_tick for new data

        Read o_rx_data when done tick is high

    For transmitting:

        Apply data to i_tx_data

        Pulse i_tx_start high

        Wait for o_tx_done_tick before sending next byte

## Timing

    The module uses 16x oversampling for reliable data sampling

    Baud rate is derived from the system clock (default 50MHz → 19200 baud)

    Timing is handled automatically by the baud rate generator

## Notes

    The UART uses standard format: 1 start bit, 8 data bits, 1 stop bit

    No parity bit is implemented

    The receiver detects start bits by monitoring for high-to-low transitions