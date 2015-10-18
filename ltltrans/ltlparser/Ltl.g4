grammar Ltl;

// Based on the Promela grammar documented at: http://spinroot.com/spin/Man/ltl.html

exp : '(' exp ')'           |
      PROP                  |
      unop WS? exp          |
      exp WS? binop WS? exp ;

unop : 'G' | 'F' | 'X' | '~' ;
binop : 'U' | 'W' | '^' | 'v' | '<->' | '->' ;

PROP  : [A-Za-z^GFXUW] ;
WS    : [ \t]+      ;
