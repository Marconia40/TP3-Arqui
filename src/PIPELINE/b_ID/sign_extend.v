`timescale 1ns / 1ps

module sign_extend#(
        parameter SIZE_IN = 16,
        parameter SIZE_OUT = 32
    )
    (
        input [SIZE_IN-1:0]  i_data,
        output reg [SIZE_OUT-1:0] o_data
    );

    always@(*) begin
        o_data[SIZE_IN-1:0]       = i_data[SIZE_IN-1:0];
        o_data[SIZE_OUT-1:SIZE_IN]  = {SIZE_IN{i_data[SIZE_IN-1]}}; // se extiende el signo de i_data[15]
    end    
endmodule