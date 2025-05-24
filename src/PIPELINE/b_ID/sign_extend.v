`timescale 1ns / 1ps

module sign_extend#(
        parameter HALF_IN_SIZE = 16,
        parameter OUT_SIZE = 32
    )
    (
        input [HALF_IN_SIZE-1:0]  i_data,
        output reg [OUT_SIZE-1:0] o_data
    );

    always@(*) begin
        o_data[HALF_IN_SIZE-1:0]       = i_data[HALF_IN_SIZE-1:0];
        o_data[OUT_SIZE-1:HALF_IN_SIZE]  = {HALF_IN_SIZE{i_data[HALF_IN_SIZE-1]}}; // se extiende el signo de i_data[15]
    end  
endmodule