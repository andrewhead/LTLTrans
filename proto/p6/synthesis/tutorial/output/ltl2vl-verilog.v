//G(F(timer=1)) -> (G(fl=1 -> (fl=1 U timer=1)) *                  G(hl=1 -> (hl=1 U timer=1)) *                  G(car=1 -> F(fl=1)) *                  G(F(hl=1)) *                  G(!(hl=1 * fl=1)))
module synthesis(hl,fl,clk,car,timer);
  input  clk,car,timer;
  output hl,fl;
  wire clk,hl,fl,car,timer;
  reg [1:0] state;

   assign hl = (state == 0)||(state == 1);
   assign fl = (state == 2);

  initial begin
    state = 2; //n14_1n18_1
  end
  always @(posedge clk) begin
    case(state)
    0: begin //n14_1n18_1n16_1
      if (timer==1) state = 2;
      if (timer==0) state = 0;
    end
    1: begin //n18_1n6_0
      if (timer==0 && car==0) state = 1;
      if (timer==1) state = 2;
      if (car==1 && timer==0) state = 0;
    end
    2: begin //n14_1n18_1
      if (timer==1) state = 1;
      if (timer==0) state = 2;
    end
    endcase
  end
endmodule //synthesis
