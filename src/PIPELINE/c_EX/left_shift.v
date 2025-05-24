`timescale 1ns / 1ps

module left_shift#(
        parameter PC_SIZE = 32
    )
    (
        input   [PC_SIZE-1:0] i_data,
        
        output  [PC_SIZE-1:0] o_result
    );
    
    assign o_result = i_data << 2;
    
endmodule