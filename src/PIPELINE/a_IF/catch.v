    `timescale 1ns / 1ps

    module catch#(
            parameter SIZE = 32
        )
        (
            input i_clock,
            input [SIZE-1:0] i_next_pc,

            output [SIZE-1:0] o_next_pc
        );

        reg [SIZE-1:0] next_pc;

        always@(posedge i_clock)begin
            next_pc <= i_next_pc;
        end

        assign o_next_pc = next_pc;

    endmodule