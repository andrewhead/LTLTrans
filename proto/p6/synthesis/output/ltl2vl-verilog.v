//(G(cn=1 -> F(gn=1)) *G(ce=1 -> F(ge=1)) *G(!(gn=1 * ge=1)) *G(!(gn=1 * rn=1)) *G(!(ge=1 * re=1)) *G(gn=1 -> re=1) *G(ge=1 -> rn=1))
module synthesis(rn,ge,re,gn,clk,ce,cn);
  input  clk,ce,cn;
  output rn,ge,re,gn;
  wire clk,rn,ge,re,gn,ce,cn;
  reg [2:0] state;

   assign gn = (state == 0)||(state == 4);
   assign re = (state == 0)||(state == 4);
   assign rn = (state == 1)||(state == 2)||(state == 3);
   assign ge = (state == 1)||(state == 2)||(state == 3);

  initial begin
    state = 2; //n11_1
  end
  always @(posedge clk) begin
    case(state)
    0: begin //n8_1n11_1-n8_1
      if (ce==0) state = 2;
      if (ce==1) state = 4;
    end
    1: begin //n7_1n11_1-n7_1
      if (cn==1) state = 3;
      if (cn==0) state = 2;
    end
    2: begin //n11_1
      if (cn==0) state = 2;
      if (cn==1) state = 0;
    end
    3: begin //n8_1n11_1
      state = 0;
    end
    4: begin //n7_1n11_1
      state = 1;
    end
    endcase
  end
endmodule //synthesis
