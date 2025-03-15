    `timescale 1ns / 1ps

    module program_counter#(
            parameter PC_SIZE = 32
        )    
        (
            input                   i_enable,   // from PC
            input                   i_clock,
            input                   i_reset,
            input   [PC_SIZE-1:0]   i_mux_pc,
            input                   i_pc_stall, // from UNIT STALL1 - > (normal 0) - > (stall pc 1)
            
            output  [PC_SIZE-1:0]      o_pc
        );
        
        reg [PC_SIZE-1:0]      pc_reg;
        
        assign o_pc = pc_reg;
        
        initial begin
            pc_reg = {PC_SIZE{1'b0}};
        end
        
        always@(posedge i_clock)
            if(i_reset) begin
                pc_reg <= {PC_SIZE{1'b0}};
            end
            else if(i_enable) begin
                
                if(!i_pc_stall)begin
                    pc_reg <= pc_reg;
                end
                else begin
                    pc_reg <= i_mux_pc;
                end
            end
            else begin
                pc_reg <= pc_reg;
            end
        
    endmodule