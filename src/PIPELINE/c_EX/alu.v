`timescale 1ns / 1ps

module alu#(
    parameter REG_SIZE = 32,
    parameter ALU_CTRL_SIZE = 4
)    
(
    input signed [REG_SIZE-1 : 0]         i_A,
    input signed [REG_SIZE-1 : 0]         i_B,
    input        [ALU_CTRL_SIZE-1 : 0]    i_alu_ctrl, // Codigo de operacion que viene de la alu_control
    output                                o_zero,
    output reg signed [REG_SIZE-1 : 0]    o_result 
);

    always@(*) begin
        case(i_alu_ctrl)
            4'h0 : o_result = i_B << i_A;      // SLL Shift left logical (r1<<r2) y SLLV
            4'h1 : o_result = i_B >> i_A;      // SRL Shift right logical (r1>>r2) y SRLV
            4'h2 : o_result = i_B >>> i_A;     // SRA Shift right arithmetic (r1>>>r2) y SRAV
            4'h3 : o_result = i_A + i_B;       // ADD/ADDU Sum (r1+r2)
            4'h4 : o_result = i_A - i_B;       // SUB/SUBU Substract (r1-r2)
            4'h5 : o_result = i_A & i_B;       // AND Logical and (r1&r2)
            4'h6 : o_result = i_A | i_B;       // OR Logical or (r1|r2)
            4'h7 : o_result = i_A ^ i_B;       // XOR Logical xor (r1^r2)
            4'h8 : o_result = ~(i_A | i_B);    // NOR Logical nor ~(r1|r2)
            4'h9 : o_result = (i_A < i_B);     // SLT Compare (signed: r1<r2)
            4'hA : o_result = i_A < i_B;       // SLTU Compare (unsigned: r1<r2)
            4'hB : o_result = i_B << 16;       // LUI Load upper immediate
            4'hC : o_result = (i_A == i_B);    // BEQ Equality check
            default : o_result = {REG_SIZE{1'b0}}; // Default: output 0
        endcase
    end

    assign o_zero = (o_result == 0);
       
endmodule
