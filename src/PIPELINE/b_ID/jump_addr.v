`timescale 1ns / 1ps

module jump_addr#(
		parameter JUMP_ADDR_SIZE       = 26,    // Jump addr in J type instructions          
		parameter PC_SIZE         = 32,            
		parameter UPPER_SIZE   = 4,     // Number of bits of upper PC+1
		parameter LOWER_SIZE = 2
	) 
	( 
		input i_clock,
		input i_reset,
		input i_enable,
		input [JUMP_ADDR_SIZE-1:0]     i_inst,                           
		input [UPPER_SIZE-1:0] i_next_pc,   // PC+1[31:28]                
		output  [PC_SIZE-1:0]  o_jump_addr         
	);

	reg [PC_SIZE-1:0]  jump_addr;

    always@(posedge i_clock) begin
		if(i_reset) begin
			jump_addr <= 0;
		end  
		else if(i_enable) begin
			jump_addr[LOWER_SIZE-1:0] 		<= 2'b00; 		// [1:0]
			jump_addr[JUMP_ADDR_SIZE+1:LOWER_SIZE] 	<= i_inst; 		// [27:2]
			jump_addr[PC_SIZE-1:JUMP_ADDR_SIZE+2] 		<= i_next_pc; 	// [31:28]
		end
		else begin
			jump_addr <= jump_addr;
		end  
    end

	assign o_jump_addr = jump_addr;
endmodule