`timescale 1ns / 1ps

module rx_uart#(
        parameter DATA_BITS = 8,      // Number of bits of data
        parameter TICKS = 16,  // sampling rate for 19200 bauds
        parameter STATE_SIZE = 2
    )
    (
        input i_clock, 
        input i_reset,
        input i_rx,     // UART bits
        input i_s_tick, // baudrate generator tick
        output reg o_rx_done_tick,
        output [DATA_BITS-1:0] o_data 
    );

    localparam [STATE_SIZE - 1 : 0] IDLE  = 2'b00;
    localparam [STATE_SIZE - 1 : 0] START = 2'b01;
    localparam [STATE_SIZE - 1 : 0] DATA  = 2'b10;
    localparam [STATE_SIZE - 1 : 0] STOP  = 2'b11;

    reg [1:0] state, next_state;
    reg [3:0] tick_counter, next_tick_counter;
    reg [2:0] data_counter, next_data_counter;
    reg [7:0] shiftreg, next_shiftreg; //shiftreg

    always @(posedge i_clock) begin

        if (i_reset) begin
            state           <= IDLE;
            tick_counter    <= 0;
            data_counter    <= 0;
            shiftreg        <= 0;
        end
        else begin
            state           <= next_state;
            tick_counter    <= next_tick_counter;
            data_counter    <= next_data_counter;
            shiftreg        <= next_shiftreg;
        end
    end

    always @(*) begin

    next_state          = state;
    o_rx_done_tick      = 1'b0;
    next_tick_counter   = tick_counter;
    next_data_counter   = data_counter;
    next_shiftreg       = shiftreg;

        case (state)
            IDLE: begin
                if(~i_rx) begin
                    next_state          = START;
                    next_tick_counter   = 0;
                end
            end
            START: begin
                if(i_s_tick) begin
                    if(tick_counter == 7) begin
                        next_state          = DATA;
                        next_tick_counter   = 0;
                        next_data_counter   = 0;
                    end
                    else begin
                        next_tick_counter = tick_counter + 1;
                    end    
                end
            end
            DATA: begin
                if(i_s_tick) begin
                    if(tick_counter == (TICKS - 1)) begin
                        next_tick_counter = 0;
                        next_shiftreg = {i_rx, shiftreg[DATA_BITS-1:1]};
                        if(data_counter == (DATA_BITS - 1))
                            next_state = STOP;
                        else
                            next_data_counter = data_counter + 1;
                        end
                    else begin
                        next_tick_counter = tick_counter + 1;
                    end
                end
            end
            STOP: begin
                if(i_s_tick) begin
                    if(tick_counter == (TICKS - 1)) begin
                        next_state      = IDLE;
                        o_rx_done_tick  = 1'b1;
                    end
                    else begin
                        next_tick_counter = tick_counter + 1;
                    end       
                end
            end
        endcase   
    end

    assign o_data = shiftreg;
endmodule