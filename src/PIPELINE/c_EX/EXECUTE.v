`timescale 1ns / 1ps

module EXECUTE#(
        parameter ALU_OP_SIZE       = 6,
        parameter ALU_CTRL_SIZE     = 4,
        parameter IMM_SIZE          = 32,
        parameter PC_SIZE           = 32,
        parameter DATA_SIZE         = 32,
        parameter REG_SIZE          = 5,
        parameter FUNCTION_SIZE     = 6,
        parameter SELECT_SIZE       = 2
    )
    (
        input                   i_signed,
        input                   i_reg_write,  // WB stage flag
        input                   i_mem_to_reg, // WB stage flag
        input                   i_mem_read,   // MEM stage flag
        input                   i_mem_write,  // MEM stage flag
        input                   i_branch,     // MEM stage flag
        input                   i_alu_src,
        input                   i_reg_dest,
        input [ALU_OP_SIZE-1:0]   i_alu_op,
        input [PC_SIZE-1:0]       i_pc,
        input [DATA_SIZE-1:0]     i_data_a,
        input [DATA_SIZE-1:0]     i_data_b,
        input [IMM_SIZE-1:0]      i_immediate,
        input [DATA_SIZE-1:0]     i_shamt,
        input [REG_SIZE-1:0]      i_rt,
        input [REG_SIZE-1:0]      i_rd,
        input                   i_byte_enable,
        input                   i_halfword_enable,
        input                   i_word_enable,
        input                   i_halt,
        input [DATA_SIZE-1:0]     i_mem_fwd_data,   // forwarding
        input [DATA_SIZE-1:0]     i_wb_fwd_data,    // forwarding
        input [SELECT_SIZE-1:0]      i_fwd_a,          // FORWARDING UNIT
        input [SELECT_SIZE-1:0]      i_fwd_b,          // FORWARDING UNIT
        input [SELECT_SIZE-1:0]      i_forwarding_mux, // FORWARDING UNIT
        input                   i_jump,
        
        output                  o_signed,
        output                  o_reg_write,
        output                  o_mem_to_reg,
        output                  o_mem_read,
        output                  o_mem_write,
        output                  o_branch,
        output [PC_SIZE-1:0]      o_branch_addr,
        output                  o_zero,
        output [DATA_SIZE-1:0]    o_alu_result,
        output [DATA_SIZE-1:0]    o_data_b,
        output [REG_SIZE-1:0]     o_selected_reg,
        output                  o_byte_enable,
        output                  o_halfword_enable,
        output                  o_word_enable,
        output                  o_last_register_ctrl,
        output [PC_SIZE-1:0]      o_pc,
        output                  o_halt,
        output                  o_jump
    );
    
    wire [IMM_SIZE-1:0]       shifted_imm;
    wire [PC_SIZE-1:0]        branch_addr;
    wire [DATA_SIZE-1:0]      out_mux2_shamt_OR_dataA;
    wire [DATA_SIZE-1:0]      dataB_or_Inm;
    wire [DATA_SIZE-1:0]      alu_data_a;
    wire [DATA_SIZE-1:0]      alu_data_b;
    wire                    zero;
    wire [DATA_SIZE-1:0]      alu_result;
    wire [ALU_CTRL_SIZE-1:0]  alu_ctrl;
    wire [REG_SIZE-1:0]       RT_or_RD;
    wire [REG_SIZE-1:0]       selected_reg;
    wire [FUNCTION_SIZE-1:0]     funct_code;
    wire [DATA_SIZE-1:0]      data_b;
    
    wire                    select_shamt;
    wire                    last_register_ctrl;

    reg [REG_SIZE-1:0]        last_register = 5'd31;
    
    assign funct_code = i_immediate [FUNCTION_SIZE-1:0];
    
    adder adder_2
    (
        .i_A(i_pc),
        .i_B(shifted_imm),
        .o_result(branch_addr)
    );

    alu alu
    (
        .i_A(alu_data_a),
        .i_B(alu_data_b),
        .i_alu_ctrl(alu_ctrl),
        .o_zero(zero),
        .o_result(alu_result)
    );

    alu_ctr alu_ctr
    (
        .i_funct_code(funct_code), 
        .i_alu_op(i_alu_op),
        .o_alu_ctrl(alu_ctrl),
        .o_shamt_ctrl(select_shamt),
        .o_last_register_ctrl(last_register_ctrl)
    );

    left_shift left_shift
    (
        .i_data(i_immediate),
        .o_result(shifted_imm)
    );

    mux2 mux2_dataB_or_Inm
    (
        .i_SEL(i_alu_src),
        .i_A(i_data_b),
        .i_B(i_immediate),
        .o_data(dataB_or_Inm)
    );

    mux2 #(.NB(5)) mux2_RT_or_RD
    (
        .i_SEL(i_reg_dest),
        .i_A(i_rt),
        .i_B(i_rd),
        .o_data(RT_or_RD)
    );

    mux2 #(.NB(5)) mux2_RT_RD_or_LAST_REG
    (
        .i_SEL(last_register_ctrl),
        .i_A(RT_or_RD),
        .i_B(last_register),
        .o_data(selected_reg)
    );

    mux2 mux2_shamt_OR_dataA
    (
        .i_SEL(select_shamt),
        .i_A(i_shamt),
        .i_B(i_data_a),
        .o_data(out_mux2_shamt_OR_dataA)
    );
        
    mux4 mux4_shamt_dataA_OR_mem_data_OR_forward_data
    (
        .i_SEL(i_fwd_a),
        .i_A(out_mux2_shamt_OR_dataA), // 00
        .i_B(i_mem_fwd_data),  // 01
        .i_C(i_wb_fwd_data),   // 10
        .i_D(),
        .o_data(alu_data_a)
    );

    mux4 mux4_dataB_Inm_OR_mem_data_OR_forward_data
    (
        .i_SEL(i_fwd_b),
        .i_A(dataB_or_Inm),         // 00
        .i_B(i_mem_fwd_data),    // 01
        .i_C(i_wb_fwd_data),     // 10
        .i_D(),
        .o_data(alu_data_b)
    );

    mux4 mux4_mem_data_OR_wb_data_OR_dataB
    (   //Dato normal, Dato de WriteBack, Dato de Memoria
        .i_SEL(i_forwarding_mux),
        .i_A(i_mem_fwd_data),  // 00
        .i_B(i_wb_fwd_data),   // 01
        .i_C(i_data_b),        // 10 dato normal
        .i_D(),
        .o_data(data_b)
    );

    assign o_signed              = i_signed;
    assign o_reg_write           = i_reg_write;
    assign o_mem_to_reg          = i_mem_to_reg;
    assign o_mem_read            = i_mem_read;
    assign o_mem_write           = i_mem_write;
    assign o_branch              = i_branch;
    assign o_branch_addr         = branch_addr;
    assign o_zero                = zero;
    assign o_alu_result          = alu_result;
    assign o_data_b              = data_b; 
    assign o_selected_reg        = selected_reg;
    assign o_byte_enable         = i_byte_enable;
    assign o_halfword_enable     = i_halfword_enable;
    assign o_word_enable         = i_word_enable;
    assign o_last_register_ctrl  = last_register_ctrl;
    assign o_pc                  = i_pc;
    assign o_halt                = i_halt;
    assign o_jump                = i_jump;

endmodule