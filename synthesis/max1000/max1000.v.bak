module max1000 (clk_in, reset_in, rs232_tx, rs232_rx, leds);

  input clk_in;
  input reset_in;
  input rs232_rx;
  //output rs232_cts;
  output rs232_tx;
  //output rs232_rtr;
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
	 wire pwm;
	 wire [7:0] int_leds;
	  
    soc soc_0(
	   .clk(clk_50), 
	   .stdout_tx(rs232_tx), 
	   .leds_out(int_leds), 	
		.pwm_pwm_out(pwm),
	   .stdin_rx(rs232_rx)
	 );
	 
	 assign leds = int_leds | pwm; //use first LED as PWM
	 
////////////////////////////////////////////////////////////////////////////////


endmodule
