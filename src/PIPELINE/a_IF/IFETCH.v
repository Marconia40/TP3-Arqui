`timescale 1ns / 1ps

module IFETCH#(
        parameter PC_SIZE             = 32,
        parameter INSTRUCTION_SIZE    = 32,
        parameter INSTMEM_SIZE     = 8, 
        parameter MEM_SIZE      = 8
    )
    (
        input                       i_clock,
        input                       i_branch,               // 1 -> Hay branch, 0 -> No hay branch
        input                       i_j_jal,                // 1 -> Hay jump, 0 -> No hay jump
        input                       i_jr_jalr,              // 1 -> Hay jump, 0 -> No hay jump
        input                       i_pc_enable,            // Enable PC
        input                       i_pc_reset,             // Reset PC
        input                       i_read_enable,          // Read Enable for instruccions mem
        input                       i_instru_mem_enable,    // Instruccion Memory enable
        input                       i_write_enable,         // Instruccion Memory Write enable
        input  [MEM_SIZE-1:0]       i_write_data,           // Data To write in Instruccion Memory 
        input  [INSTMEM_SIZE-1:0]   i_write_addr,           // Addr used for write in Instruccion Memory 
        input  [PC_SIZE-1:0]        i_branch_addr,          // Branching
        input  [PC_SIZE-1:0]        i_jump_addr,            // J y JAL
        input  [PC_SIZE-1:0]        i_data_last_register,   // JR y JALR
        input                       i_pc_stall,             // STALL UNIT

        output [PC_SIZE-1:0]          o_last_pc,              // PC
        output [PC_SIZE-1:0]          o_adder_result,         // PC+4
        output [INSTRUCTION_SIZE-1:0] o_instruction
    );

    wire [PC_SIZE-1:0]            new_pc_value;
    wire [PC_SIZE-1:0]            adder_result;   
    wire [PC_SIZE-1:0]            mux2_1_output;
    wire [PC_SIZE-1:0]            mux2_2_output;
    wire [PC_SIZE-1:0]            mux2_3_output;
    //wire [PC_SIZE-1:0]            jump_addr;
    wire [INSTRUCTION_SIZE-1:0]   instruction;

    reg [PC_SIZE-1:0]    pc_constant = 32'd4;

    program_counter program_counter
    (
        .i_enable(i_pc_enable),
        .i_clock(i_clock),
        .i_reset(i_pc_reset),
        .i_mux_pc(mux2_3_output),
        .i_pc_stall(i_pc_stall),
        .o_pc(new_pc_value)
    );

    adder adder
    (
        .i_A(new_pc_value), 
        .i_B(pc_constant),
        .o_result(adder_result)
    );

    latch latch
    (
        .i_clock(i_clock),
        .i_next_pc(adder_result),
        .o_next_pc(o_adder_result)
    );

    mux2 mux2_1
    (
        .i_SEL(i_branch),
        .i_A(adder_result),     // PC+1
        .i_B(i_branch_addr),    // branch
        .o_data(mux2_1_output)
    );

    mux2 mux2_2
    (
        .i_SEL(i_j_jal),
        .i_A(mux2_1_output),
        .i_B(i_jump_addr),
        .o_data(mux2_2_output)
    );

    mux2 mux2_3
    (
        .i_SEL(i_jr_jalr),
        .i_A(mux2_2_output),
        .i_B(i_data_last_register),
        .o_data(mux2_3_output)
    );            

    inst_mem inst_mem
    (
        .i_clock(i_clock),
        .i_enable(i_instru_mem_enable),
        .i_write_enable(i_write_enable),
        .i_read_enable(i_read_enable),
        .i_write_data(i_write_data),
        .i_write_addr(i_write_addr),
        .i_read_addr(new_pc_value),
        .o_read_data(instruction)
    );

    assign o_instruction     = instruction;
    assign o_last_pc         = new_pc_value;
    
endmodule