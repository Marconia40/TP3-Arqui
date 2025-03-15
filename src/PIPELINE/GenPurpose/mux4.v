`timescale 1ns / 1ps

module mux4#(
        parameter   SIZE = 32,
        parameter   SIZE_SELECT = 2   
    )
    (
        input  [SIZE_SELECT-1:0]     i_SEL,
        input  [SIZE-1:0]            i_A,
        input  [SIZE-1:0]            i_B,
        input  [SIZE-1:0]            i_C,
        input  [SIZE-1:0]            i_D,
        output [SIZE-1:0]            o_data
    
    );
    
    reg [SIZE-1:0] aux_reg;
    
    always @ (*) begin
        case (i_SEL)
            2'b00 : aux_reg <= i_A;
            2'b01 : aux_reg <= i_B;
            2'b10 : aux_reg <= i_C;
            2'b11 : aux_reg <= i_D;    
        endcase
    end
    
    assign o_data = aux_reg;

endmodule