from converter import *

def run_demo():
    #V1 = VarRule(Var("m"), "move", noun = "robot")
    #V1_neg  = VarRule(NegVar("m"), "stop", noun = "robot")
    #V2 = VarRule(Var("p"), "push", noun = "button")
    #V3 = VarRule(Var("d"), "open", noun = "door")
    #V3_neg = VarRule(NegVar("d"), ["close", "shut"], noun = "door")
    V4 = VarRule(Var("a"), "sound", noun = "alarm")
    V5 = VarRule(Var("f"), "flash", noun = "light")


    print "The variables are:"
    print "p: The button is pushed"
    print "d: The door is open"
    while True:
        s = raw_input("What would you like to translate? >>> ")
        if s == "quit":
            break
        c = Converter(s, [V4, V5])
        a = c.get_statement()
        print_ltl(a)
        
        
