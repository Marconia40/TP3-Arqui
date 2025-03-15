`timescale 1ns / 1ps

module WBACK#(
        parameter DATA_SIZE = 32,
        parameter REG_SIZE  = 5,
        parameter PC_SIZE   = 32
    )
    (   input                       i_reg_write,            // Pasamano de que SI se escribe en un registro
        input                       i_mem_to_reg,           // MUX selector de ALU RESULT y VALOR OBTENIDO DE LA MEMORIA
        input [DATA_SIZE-1:0]       i_mem_data,             // i_mem_to_reg = 1
        input [DATA_SIZE-1:0]       i_alu_result,           // i_mem_to_reg = 0
        input [REG_SIZE-1:0]        i_selected_reg,         // Direccion del registro donde escribir
        input                       i_last_register_ctrl,   // Si se escribe en el ultimo registro debido a JAL y JALR
        input [PC_SIZE-1:0]         i_pc,                   // Valor de Program Counter
        input                       i_halt,                 // Si se genero un HALT

        output                      o_reg_write,            // Indica si se escribe en un REGISTRO
        output [DATA_SIZE-1:0]      o_selected_data,        // Valor que se escribe
        output [REG_SIZE-1:0]       o_selected_reg,         // Valor de la direccion DONDE se escribe
        output                      o_halt                  // HALT
    );

    wire [DATA_SIZE-1:0]    mux2_5_data;

    mux2 mux2_10
    (
        .i_SEL(i_mem_to_reg),
        .i_A(i_alu_result),
        .i_B(i_mem_data),
        .o_data(mux2_5_data)
    );

    mux2 mux2_11
    (
        .i_SEL(i_last_register_ctrl),           // JAL Y JALR guardan el valor de PC en LAST REGISTER in bank register
        .i_A(mux2_5_data),
        .i_B(i_pc),
        .o_data(o_selected_data)
    );
    
    assign o_reg_write       = i_reg_write;
    assign o_selected_reg    = i_selected_reg;
    assign o_halt            = i_halt;
endmodule