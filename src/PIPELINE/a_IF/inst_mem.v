    `timescale 1ns / 1ps

    module inst_mem#(
    parameter ADDR_SIZE       = 8,
    parameter ADDR_RW         = 32,
    parameter MEM_SIZE        = 8,                 // Specify RAM data width
    parameter MEM_LARGE       = 256,               // Specify RAM depth (number of entries)
    parameter INST_SIZE       = 32
    ) 
    (
    input                       i_clock,
    input                       i_enable,               // Debug Unit Control                            
    input                       i_read_enable,          
    input                       i_write_enable,         // Debug Unit Control   
    input  [MEM_SIZE-1:0]       i_write_data,           // Debug Unit Control
    input  [ADDR_SIZE-1:0]      i_write_addr,           // Debug Unit Control
    input  [ADDR_RW-1:0]        i_read_addr,            // Read addr bus, width determined from RAM_DEPTH
    output [INST_SIZE-1:0]      o_read_data             // RAM output data
    );

    reg [MEM_SIZE-1:0] BRAM [MEM_LARGE-1:0];
    reg [INST_SIZE-1:0] ram_data = {INST_SIZE{1'b0}};

    generate
        integer ram_index;
        initial
        for (ram_index = 0; ram_index < MEM_LARGE; ram_index = ram_index + 1)
            BRAM[ram_index] = {MEM_SIZE{1'b0}};
    endgenerate

    always @(posedge i_clock) begin
        if(i_enable) begin
            if (i_read_enable) begin
                ram_data[31:24] <= BRAM[i_read_addr];
                ram_data[23:16] <= BRAM[i_read_addr+1];
                ram_data[15:8]  <= BRAM[i_read_addr+2];
                ram_data[7:0]   <= BRAM[i_read_addr+3];
            end
            else begin
                ram_data <= {INST_SIZE{1'b0}};
            end
            
            if(i_write_enable) begin
                // Para debug unit
                BRAM[i_write_addr]   <= i_write_data;
            end
        end
    end

    assign o_read_data = ram_data;

    endmodule		