`timescale 1ns / 1ps

module alu#(
        parameter DATA_SIZE    = 32,
        parameter ALU_CTRL_SIZE = 4
    )    
    (
        input signed [DATA_SIZE-1 : 0]         i_A,
        input signed [DATA_SIZE-1 : 0]         i_B,
        input       [ALU_CTRL_SIZE-1 : 0]    i_alu_ctrl, // codigo de operacion que viene de la alu_control
        output                              o_zero,
        output reg signed [DATA_SIZE-1 : 0]    o_result 
    );   
    always@(*) begin
        case(i_alu_ctrl)
            4'h0 : begin
                o_result =   i_B << i_A[4:0];     // SLL/SLLV Shift left logical (rt << shamt/rs[4:0])
            end
            4'h1 : begin
                o_result =   i_B >> i_A[4:0];     // SRL/SRLV Shift right logical (rt >> shamt/rs[4:0])
            end
            4'h2 : begin
                o_result =   i_B >>> i_A[4:0];    // SRA/SRAV Shift right arithmetic (rt >>> shamt/rs[4:0])
            end
            4'h3 : begin
                o_result =   i_A + i_B;           // ADD/ADDI Sum (rs+rt/immediate)
            end
            4'h4 : begin
                o_result =   i_A - i_B;           // SUB Substract (rs-rt)
            end
            4'h5 : begin
                o_result =   i_A & i_B;       // AND Logical and (r1&r2)
            end
            4'h6 : begin
                o_result =   i_A | i_B;       // OR Logical or (r1|r2)
            end
            4'h7 : begin
                o_result =   i_A ^ i_B;       // XOR Logical xor (r1^r2)
            end
            4'h8 : begin
                o_result = ~(i_A | i_B);      // NOR Logical nor ~(r1|r2)
            end            4'h9 : begin 
                o_result =   i_A < i_B;       // SLT Compare (rs < rt)
            end
            4'ha : begin
                o_result =   i_B << 16;       // LUI - Load Upper Immediate (immediate << 16)
            end
            4'hb : begin
                o_result =   i_A == i_B;      // BEQ: resultado 1 si iguales (salta), 0 si diferentes
            end
            4'hc : begin
                o_result =   i_A != i_B;      // BNE: resultado 1 si diferentes (salta), 0 si iguales
            end
            default : begin 
                o_result =  {DATA_SIZE{1'b0}};
            end
        endcase
    end
    
    assign o_zero = o_result == 0;

endmodule
