`timescale 1ns / 1ps

module left_shift#(
        parameter BIT_SIZE = 32
    )
    (
        input   [BIT_SIZE-1:0] i_data,
        
        output  [BIT_SIZE-1:0] o_result
    );
    
    assign o_result = i_data << 2;
    
endmodule