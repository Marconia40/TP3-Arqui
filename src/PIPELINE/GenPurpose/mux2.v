`timescale 1ns / 1ps

module mux2#(
        parameter   SIZE = 32
    )
    (
        input           i_SEL,
        input  [SIZE-1:0] i_A,
        input  [SIZE-1:0] i_B,
        output [SIZE-1:0] o_data
    
    );
    
    reg [SIZE-1:0] aux_reg;
    
    always @ (*) begin
        case (i_SEL)
            1'b0 : aux_reg <= i_A;
            1'b1 : aux_reg <= i_B;
        endcase
    end
    
    assign o_data = aux_reg;

endmodule