module max1000 (clk_in, reset_in, rs232_tx, rs232_cts, rs232_rx, rs232_rtr, leds);

  input clk_in;
  input reset_in;
  input rs232_rx;
  output rs232_cts;
  output rs232_tx;
  output rs232_rtr;
  output [7:0] leds;


////////////////////////////////////////////////////////////////////////////////
//RESET AND CLOCKS
//
  wire clk_150;
  wire clk_50;
  wire clk_10;
  wire locked;
  reg locked_d;
  wire clk;
  reg rst;
  wire rst_n;
  xcvr_pll pll_0( areset, clk_in, clk_150, clk_10, clk_50, locked);
  assign clk = clk_150;
  always@(posedge clk_50) begin
    locked_d <= locked;
    rst <= ~locked_d;
  end
  assign rst_n = ~rst;


////////////////////////////////////////////////////////////////////////////////
//Chips-V SoC
//

    wire [31:0] debug_rx;
    wire debug_rx_stb;
    wire debug_rx_ack;

    wire [31:0] debug_tx;
    wire debug_tx_stb;
    wire debug_tx_ack;	 
	  
    soc soc_0(
	   .clk(clk_50), 
	   .stdout_ready_in(debug_tx_ack), 
	   .stdout_valid_out(debug_tx_stb), 
	   .stdout_out(debug_tx), 
		
	   .leds_out(leds), 	
		
		.stdin_valid_in(debug_rx_stb), 
	   .stdin_in(debug_rx), 
	   .stdin_ready_out(debug_rx_ack)
	 );
	 
////////////////////////////////////////////////////////////////////////////////
//Uart
//

    serial_output #(
        .clock_frequency(50000000),
        .baud_rate(115200)
    )
    serial_output_0(
        .clk(clk_50),
        .rst(rst),
        .tx(rs232_tx),
		  .cts(rs232_cts),
       
        .in1(debug_tx[7:0]),
        .in1_stb(debug_tx_stb),
        .in1_ack(debug_tx_ack)
    );

    serial_input #(
        .clock_frequency(50000000),
        .baud_rate(115200)
    )
    serial_input_0(
        .clk(clk_50),
        .rst(rst),
        .rx(rs232_rx),
		  .rtr(rs232_rtr),
       
        .out1(debug_rx[7:0]),
        .out1_stb(debug_rx_stb),
        .out1_ack(debug_rx_ack)
    );

endmodule
