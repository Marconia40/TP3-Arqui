`timescale 1ns / 1ps

module mem_data#(
  parameter MEMORY_SIZE = 32,              // Ancho de palabra, osea de cada valore
  parameter MEMORY_DEPTH = 32,              // Profundidad de la memoria, esta es de solo 32, es una memoria 32x32
  parameter ADDR_SIZE = 5,					// Ancho de la direccion
  parameter DATA_SIZE = 32
) 
(
  input                 	i_clock,        // Clock
  input                 	i_enable,       // Enable
  input                 	i_write, 		// Enable Write
  input                 	i_read,  		// Enable Read 
  input  [ADDR_SIZE-1:0]  	i_read_addr,   	// addr for write and read
  input  [DATA_SIZE-1:0]  	i_write_data,   // Data for write
  output [DATA_SIZE-1:0]  	o_read_data     // Data readed
);

	reg [MEMORY_SIZE-1:0] BRAM [MEMORY_DEPTH-1:0];
	reg [DATA_SIZE-1:0] ram_data = {DATA_SIZE{1'b0}};

	generate
		integer ram_index;
		initial
			for (ram_index = 0; ram_index < MEMORY_DEPTH; ram_index = ram_index + 1)
				BRAM[ram_index] = {MEMORY_SIZE{1'b0}};
	endgenerate


	always@(posedge i_clock) begin
		if(i_enable) begin
			// Escritura
			if(i_write) begin
				BRAM[i_read_addr] <= i_write_data;
			end	
			else begin
				BRAM[i_read_addr] <= BRAM[i_read_addr];
			end
			
			// Lectura
			if(i_read) begin
				ram_data		<= BRAM[i_read_addr];
			end
			else begin
				ram_data		<= 32'b0;
			end
		end
	end

	assign o_read_data = ram_data;

endmodule