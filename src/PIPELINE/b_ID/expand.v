`timescale 1ns / 1ps

module expand#(
        parameter EXP_IN_SIZE   = 5,
        parameter OUT_SIZE  = 32
    )
    (
        input [EXP_IN_SIZE-1:0]       i_data,
        output reg [OUT_SIZE-1:0] o_data
    );

    always@(*) begin
        o_data = { {27{1'b0}}, i_data };
    end    
endmodule