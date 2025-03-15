`timescale 1ns / 1ps

module expand#(
        parameter SIZE_IN = 5,
        parameter SIZE_OUT = 32
    )
    (
        input [SIZE_IN-1:0]       i_data,
        output reg [SIZE_OUT-1:0] o_data
    );

    always@(*) begin
        o_data = {27'b0, i_data};
    end    
endmodule