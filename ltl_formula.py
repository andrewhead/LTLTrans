import sys, random

random.seed()
bool_opers = ["&", "|", "->"]
un_temp_opers = ["F", "G", "X"]
bin_temp_opers = ["U", "W"]

class Statement:
    def __init__(self, oper = False, var = False, left = False, right = False, neg = False):
        self.operator = oper
        self.left_substatement = left
        self.right_substatement = right
        self.is_negative = neg
        self.variable = var
        if right:
            self.is_unary = False
        else:
            self.is_unary = True
        if self.variable and (self.left_substatement or self.right_substatement or not self.is_unary):
            print("error: ill-formed statement")
    def print_statement(self):
        #print self.variable, self.operator,
        if self.is_negative:
            sys.stdout.write("~")
        if self.variable:
            sys.stdout.write(self.variable)
        elif self.is_unary:
            sys.stdout.write(self.operator)
            self.left_substatement.print_statement()
        else:
            sys.stdout.write("(")
            self.left_substatement.print_statement()
            print "", self.operator, "",
            self.right_substatement.print_statement()
            sys.stdout.write(")")
    def distribute_negatives(self, opers = bin_temp_opers + bool_opers + un_temp_opers):
        negative_operator = {"&":"|", "|":"&", "U":"R", "R":"U", "F":"G", "G":"F", "X":"X"} #Figure out what to do for W
        if self.variable:
            return
        if self.is_negative:
            self.is_negative = False
            if self.operator in opers:
                if self.operator == "->":
                    self.right_substatement.is_negative = not self.right_substatement.is_negative
                    self.operator = "&"
                else:
                    if self.right_substatement:
                        self.right_substatement.is_negative = not self.right_substatement.is_negative
                    self.left_substatement.is_negative = not self.left_substatement.is_negative
                    self.operator = negative_operator[self.operator]
        if self.right_substatement:
                self.right_substatement.distribute_negatives(opers)
        self.left_substatement.distribute_negatives(opers)
    def convert_to_english(self):
        sentence = ""
        if self.variable:
            if self.is_negative:
                sentence += self.variable + " is false "
            else:
                sentence += self.variable + " is true "
        elif self.operator and self.is_unary:
            if self.operator == "F" and not self.is_negative:
                sentence += " it will eventually be the case that "
            elif self.operator == "F" and self.is_negative:
                sentence += " it will never be the case that "
            elif self.operator == "G" and not self.is_negative:
                sentence += " it will always be the case that "
            elif self.operator == "G" and self.is_negative:
                sentence += " it will not always be the case that "
            elif self.operator == "X" and not self.is_negative:
                sentence += " in the next step, it will be the case that "
            elif self.operator == "X" and self.is_negative:
                sentence += " in the next step, it will not be the case that "
            else:
                sentence += self.operator
            sentence += self.left_substatement.convert_to_english()
        elif self.operator and not self.is_unary:
            sentence += self.left_substatement.convert_to_english()
            if self.operator == "U" and not self.is_negative:
                sentence += "at until "
            elif self.operator == "W": 
                sentence += " at least until " #may not be best way to do it
            elif self.operator == "&":
                sentence += " and "
            elif self.operator == "->":
                sentence += " implies "
            elif self.operator == "|":
                sentence += " or "
            else:
                sentence += self.operator
            sentence += self.right_substatement.convert_to_english()
        else:
            return "ERROR"
        return sentence
    def english(self):
        s = self.convert_to_english()
        s = s.split()
        t = " ".join(s)
        t = t[:1].upper() + t[1:]
        t += "."
        return t
    def convert_to_english2(self):
        sentence = ""
        if self.variable:
            if self.is_negative:
                sentence += self.variable + " is false "
            else:
                sentence += self.variable + " is true "
        elif self.operator and self.is_unary:
            left_sent = self.left_substatement.convert_to_english()
            if self.operator == "F" and not self.is_negative:
                sentence += " the case that "
                sentence += left_sent
                sentence += " will eventually hold "
            elif self.operator == "F" and self.is_negative:
                sentence += " the case that "
                sentence += left_sent
                sentence += " will never hold "
            elif self.operator == "G" and not self.is_negative:
                sentence += " the case that "
                sentence += left_sent
                sentence += " will always hold "
            elif self.operator == "G" and self.is_negative:
                sentence += " the case that "
                sentence += left_sent
                sentence += " will not always hold "
            elif self.operator == "X" and not self.is_negative:
                sentence += left_sent
                sentence += " will hold in the next step "
            elif self.operator == "X" and self.is_negative:
                sentence += left_sent
                sentence += " will not hold in the next step "
            else:
                sentence += self.operator
        elif self.operator and not self.is_unary:
            left_sent = self.left_substatement.convert_to_english()
            right_sent = self.right_substatement.convert_to_english()
            if self.operator == "U" and not self.is_negative:
                sentence += left_sent
                sentence += " until "
                sentence += right_sent
            elif self.operator == "W" and not self.is_negative:
                sentence += left_sent
                sentence += " until " #may not be best way to do it
                sentence + right_sent
                sentence += " which may not occur "
            elif self.operator == "&" and not self.is_negative:
                sentence += left_sent
                sentence += " and "
                sentence += right_sent
            elif self.operator == "&" and self.is_negative:
                sentence += " it is not the case that both "
                sentence += left_sent
                sentence += " and "
                sentence += right_sent
            elif self.operator == "->":
                sentence += " if "
                sentence += left_sent
                sentence += " then "
                sentence += right_sent
            elif self.operator == "|" and not self.is_negative:
                sentence += left_sent
                sentence += " or "
                sentence += right_sent
            elif self.operator == "|" and self.is_negative:
                sentence += " neither "
                sentence += left_sent
                sentence += " nor "
                sentence += right_sent
            else:
                sentence += left_sent
                sentence += self.operator
                sentence += right_sent
        else:
            return "ERROR"
        return sentence
        
                
#Boolean Statements

def Var(var_name):
    return Statement(var = var_name)

def NegVar(var_name):
    return Statement(var = var_name, neg = True)

def And(s1, s2):
    return Statement(oper = "&", left = s1, right = s2)

def Nand(s1, s2):
    return Statement(oper = "&", left = s1, right = s2, neg = True)

def Or(s1, s2):
    return Statement(oper = "|", left = s1, right = s2)

def Nor(s1, s2):
    return Statement(oper = "|", left = s1, right = s2, neg = True)

def If(s1, s2):
    return Statement(oper = "->", left = s1, right = s2)

def NegIf(s1, s2):
    return Statement(oper = "->", left = s1, right = s2, neg = True)

#LTL Statements

def F(s):
    return Statement(oper = "F", left = s)

def NegF(s):
    return Statement(oper = "F", left = s, neg = True)

def G(s):
    return Statement(oper = "G", left = s)

def NegG(s):
    return Statement(oper = "G", left = s, neg = True)

def X(s):
    return Statement(oper = "X", left = s)

def NegX(s):
    return Statement(oper = "X", left = s, neg = True)

def U(s1, s2):
    return Statement(oper = "U", left = s1, right = s2)

def NegU(s1, s2):
    return Statement(oper = "U", left = s1, right = s2, neg = True)

def W(s1, s2):
    return Statement(oper = "W", left = s1, right = s2)

def NegW(s1, s2):
    return Statement(oper = "W", left = s1, right = s2, neg = True)

#LTL Templates

def Bool(s1, s2):
    return Statement(oper = "bool", left = s1, right = s2)

#unary temporal operator
def UnTemp(s):
    return Statement(oper = "untemp", left = s)

#Binary Temporal Operator
def BinTemp(s1, s2):
    return Statement(oper = "bintemp", left = s1, right = s2)

def FillTemplates(temp, unary_operators, binary_operators, neg_prob = 0):
    if not temp:
        return False
    s = Statement()
    #s.is_negative = temp.is_negative
    if random.random() <= neg_prob:
        s.is_negative = True
    s.is_unary = temp.is_unary
    s.variable = temp.variable
    s.left_substatement = FillTemplates(temp.left_substatement, unary_operators, binary_operators, neg_prob)
    s.right_substatement = FillTemplates(temp.right_substatement, unary_operators, binary_operators, neg_prob)
    if temp.operator == "bool":
        s.operator = random.choice(["&","|","->"])
    elif temp.operator == "untemp":
        if not unary_operators:
            print "error: no valid unary temporal operators were provided"
            return False
        s.operator = random.choice(unary_operators)
    elif temp.operator == "bintemp":
        if not binary_operators:
            print "error: no valid binary temporal operators were provided"
            return False
        s.operator = random.choice(binary_operators)
    else:
        s.operator = temp.operator
    return s
        
        
#Examples

# (p|~q)&(q->~r)
e1 = And( Or(Var("p"), NegVar("q")), If(Var("q"), NegVar("r")))
#e1.print_statement()
#print ""
#print e1.english()

#F(p U q)
e2 = F(U(Var("p"), Var("q")))
#e2.print_statement()
#print ""
#print e2.english()

#G(p -> Xq)
e3 = G(If(Var("p"), X(Var("q"))))
#e3.print_statement()
#print ""
#print e3.english()

e4 = UnTemp(Bool(Var("p"), Var("q")))
e4 = FillTemplates(e4, ["F", "X"], [])
#e4.print_statement()
#print ""
#print e4.english()

s = Bool( UnTemp( Var("p")), BinTemp(Var("q"), NegVar("r")))
r = FillTemplates(s, ["F","G", "X"], ["U", "W"], 0.5)
#r.print_statement()
#print r.english()
#Could yield, for example: (Gp -> (q  U ~r)) or (Xp & (q  W ~r))
