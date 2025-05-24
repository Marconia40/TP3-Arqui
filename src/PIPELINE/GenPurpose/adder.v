`timescale 1ns / 1ps

module adder#(
        parameter PC_SIZE = 32
    )
    (
        input   [PC_SIZE-1:0] i_A,
        input   [PC_SIZE-1:0] i_B,
        
        output  [PC_SIZE-1:0] o_result
    );
    
    assign o_result = i_A + i_B;
    
endmodule