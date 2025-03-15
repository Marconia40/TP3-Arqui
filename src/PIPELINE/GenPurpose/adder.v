`timescale 1ns / 1ps

module adder#(
        parameter SIZE = 32
    )
    (
        input   [SIZE-1:0] i_A,
        input   [SIZE-1:0] i_B,
        
        output  [SIZE-1:0] o_result
    );
    
    assign o_result = i_A + i_B;
    
endmodule