    `timescale 1ns / 1ps

    module IF_ID#(
            parameter PC_SIZE             = 32,
            parameter INST_SIZE           = 32
        )
        (
            input                       i_clock,
            input                       i_reset,
            input                       i_pipe_en,          // DEBUG UNIT
            input                       i_enable,           // STALL UNIT: 1 -> data hazard (stall) 0 -> !data_hazard
            input                       i_flush,            // STALL UNIT: 1 -> control hazards     0 -> !control_hazard
            input  [INST_SIZE-1:0]      i_instr,          
            input  [PC_SIZE-1:0]        i_next_pc,           
   
            output [PC_SIZE-1:0]        o_next_pc,
            output [INST_SIZE-1:0]      o_instr
        );

        reg [PC_SIZE-1:0]             next_pc_reg;
        reg [INST_SIZE-1:0]           instr_reg;


        always @(negedge i_clock) begin
            if(i_reset)begin
                next_pc_reg    <= {PC_SIZE{1'b0}};
                instr_reg <= {INST_SIZE{1'b0}};
            end
            else begin
                if(i_pipe_en) begin
                    if(i_enable) begin
                        if(i_flush) begin
                            next_pc_reg     <= i_next_pc;
                            instr_reg       <= {INST_SIZE{1'b0}};
                        end
                        else begin
                            next_pc_reg     <= i_next_pc;
                            instr_reg       <= i_instr;
                        end
                    end
                    else begin
                        next_pc_reg     <= next_pc_reg;
                        instr_reg       <= instr_reg;
                    end
                end
                else begin
                    next_pc_reg      <= next_pc_reg;
                    instr_reg        <= instr_reg;
                end
            end    
        end

        assign o_next_pc        = next_pc_reg;
        assign o_instr          = instr_reg;
        
    endmodule