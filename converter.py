from ltl_formula import *
import re
 

#node for a dependency tree
class Dnode:
    governor = ""
    dependents = [] #list of 2-tuples containing dependent and relation
    relations = []
    def __init__(self, g, d):
        self.governor = g
        self.dependents = d
    def add_dependent(self, dep, rel):
        self.dependents += [(dep, rel)]
        self.update_relations() ##BAD FIX THIS
    def find_dnode(self, word): #finds dnode with governor as given word. returns false, otherwise.
        print self.governor, word
        if self.governor == word:
            return self
        for d in self.dependents:
            x = d[0].find_dnode(word)
            if x:
                return x
        return False            
    def print_dnode(self):
        if not self.dependents:
            print self.governor,
            return
        print "[", self.governor, ": ",
        for d in self.dependents:
            print "(",d[1], ",",
            d[0].print_dnode()
            print ")",
        print "]",
#    def get_relations(self): #returns all relations that are applied to any children of current node
#        rel = []
#        for d in self.dependents:
#            rel += d[1] + "," + governor + "," + d[0].governor

    def update_relations(self):
        if not self.dependents:
            return set([])
        rel = set()
        for d in self.dependents:
            rel = rel.union( d[0].update_relations() )
            rel = rel.union(set(["(" + d[1] + "," + self.governor + "," + d[0].governor + ")"]))
        self.relations = list(rel)
        return rel
    """
    def apply_match(self, ltl_node, nums_to_words, root_word, rules, index): #applies a given match (from integer_variables to words) to an ltl tree and makes recursive call to apply_rules
        if str(ltl_node.variable).isdigit():
            new_root = nums_to_words[ltl_node.variable]
            new_ind = 0
            if new_root == root_word:
                new_ind = index
            ltl_temp = self.find_dnode(new_root).apply_rules(rules, new_ind)
            ltl_temp.is_negative = (ltl_temp.is_negative != ltl_node.is_negative)
            return ltl_temp
        left = ltl_node.left_substatement
        if left:
            if left.variable and str(left.variable).isdigit() and left.variable in nums_to_words:
                new_ind = 0
                new_root = nums_to_words[left.variable]
                if new_root == root_word:
                    new_ind = index
                ltl_node.left_substatement = self.find_dnode(new_root).apply_rules(rules, new_ind) 
            else:
                ltl_node.left_substatement = self.apply_match(left, nums_to_words, root_word, rules, index)
        right = ltl_node.right_substatement
        if right:
            if right.variable and str(right.variable).isdigit() and right.variable in nums_to_words:
                new_ind = 0
                new_root = nums_to_words[right.variable]
                if new_root == root_word:
                    new_ind = index
                ltl_node.right_substatement = self.find_dnode(new_root).apply_rules(rules, new_ind) 
            else:
                ltl_node.right_substatement = self.apply_match(right, nums_to_words, root_word, rules, index)
        return ltl_node
    """
    def apply_match(self, ltl_node, nums_to_words, root_word, rules, index):
        if not ltl_node:
            return None
        if ltl_node.variable:
            if str(ltl_node.variable).isdigit():
                if ltl_node.variable in nums_to_words:
                    new_ind = 0
                    new_root = nums_to_words[ltl_node.variable]
                    if new_root == root_word:
                        new_ind = index
                    d = self.find_dnode(new_root)
                    if not d:
                        print "Error:", new_root, "not in tree with", self.governor, "as root"
                        return None
                    temp = d.apply_rules(rules, new_ind)
                    print temp.is_negative, ltl_node.is_negative, self.governor
                    temp.is_negative = (temp.is_negative != ltl_node.is_negative)
                    return temp
                else:
                    print "Error: variable" + ltl_node.variable, "not in current match"
                    return None
            else:
                return ltl_node
        ltl_node.left_substatement = self.apply_match(ltl_node.left_substatement, nums_to_words, root_word, rules, index)
        ltl_node.right_substatement = self.apply_match(ltl_node.right_substatement, nums_to_words, root_word, rules, index)
        return ltl_node

    def apply_rules(self, rules, index = 0): #returns full ltl_tree applying rules to dependency_tree
        while index < len(rules):
            matches = rules[index].find_match(self)
            if matches:
                print "Match found:", matches, rules[index].requirements
                return self.apply_match(rules[index].replacement, matches, self.governor, rules, index + 1)
            print "No match found:", rules[index].requirements
            index += 1
        return False
        

#requirements: list 3-tuples of form (relation, governor, dependent)
        #any of these may be numbers to represent variables or actual words.
        #1st rule in relation applies to root node of dependency tree
#rep: ltl node with numbers (say, n) used to represents slots where get_statement(n) replaces slot in ltl tree 
class DRule:
    requirements = []
    regex_patterns = list()
    replacement = []
    def __init__(self, req, rep, t = []):
        self.requirements = req
        self.replacement = rep
        self.regex_patterns = list()
        for r in self.requirements:
            regex = "[(]"+r[0]+","
            if str(r[1]).isdigit(): #will take any word
                regex += "[\w|-]*,"
            else: #accepts only current word
                regex += r[1] + "-[0-9]*,"
            if str(r[2]).isdigit():
                regex += "[\w|-]*[)]"
            else:
                regex += r[2] + "-[0-9]*[)]"
            self.regex_patterns += [regex]
    def find_match(self, dnode):
        print "finding match for", dnode.governor, "with", self.requirements
        nums_to_words = {}
        possible_relations = []
        rels = " ".join(dnode.relations)
        match_iters = [[]]*len(self.requirements)
        changed_words = [[None,None,None]]*len(self.requirements)
        #below is important
        nums_to_words[1] = dnode.governor
        for x in range(0,len(self.requirements)):
            match_iters[x] = re.finditer(self.regex_patterns[x], rels, flags=re.IGNORECASE)
            if not match_iters[x]: #there is no valid matching
                return False
        x = 0
        current_match = [None]*len(self.requirements)
        while x < len(self.requirements):
            if x < 0:
                return False
            d1 = self.requirements[x][1]
            d2 = self.requirements[x][2]
            if changed_words[x][1]:
                del nums_to_words[d1]
            if changed_words[x][2]:
                del nums_to_words[d2]
            changed_words[x] = [None,None,None]
            i = match_iters[x]
            m = next(i, None)
            current_match[x] = m
            if not m:
                match_iters[x] = re.finditer(self.regex_patterns[x], rels, flags=re.IGNORECASE)
                x -= 1
                continue
            else:
                #print m.group()
                t = m.group()
                t = t.replace(")", "")
                t = t.replace("(", "")
                w1 = (t.split(","))[1]
                w2 = (t.split(","))[2]
                if x == 0 and w1 != dnode.governor: #first rule must come from root
                    match_iters[x] = i
                    continue
                if str(d1).isdigit():
                    if d1 in nums_to_words and nums_to_words[d1] != w1: #variables do not match up, move to next slot in current requirement
                        match_iters[x] = i
                        continue
                    elif not d1 in nums_to_words: #number is open slot, filled with w1
                        changed_words[x][1] = w1
                        nums_to_words[d1] = w1
                if str(d2).isdigit():
                    if d2 in nums_to_words and nums_to_words[d2] != w2:
                        match_iters[x] = i
                        continue
                    elif not d2 in nums_to_words:
                        changed_words[x][2] = w2
                        nums_to_words[d2] = w2
                x += 1
        return nums_to_words               
        #return [c.group() for c in current_match]
        
                        
            

    
class Converter:
    wordmap = {} #maps words to their dependency nodes
    prop_vars = []
    def __init__(self, filename, variables):
        self.prop_vars = variables
        with open(filename) as f:
            relations = f.readlines()
        t = []
        for r in relations:
            s = r[:-1]
            s = s.replace(" ", "")
            s = s.replace("(", ",")
            s = s.replace(")", "")
            l = s.split(",")
            t += [l]
            if not l[1] in self.wordmap:
                self.wordmap[l[1]] = Dnode(l[1], [])
            if not l[2] in self.wordmap:
                self.wordmap[l[2]] = Dnode(l[2], [])
        
        for l in t:
            #print "adding:", l[1], l[2], l[0]
            self.wordmap[l[1]].add_dependent(self.wordmap[l[2]], l[0])
    def get_statement(self):
        current_statement = False
        for d in self.wordmap["ROOT-0"].dependents:
            s = d[0].apply_rules(Rules + self.prop_vars)
            if not s:
                continue
            if current_statement:
                current_statement = And(current_statement, s)
            else:
                current_statement = s
        return current_statement

d1 = Dnode("moves-1", [])
d2 = Dnode("improves-2",[])
d3 = Dnode("until-3",[])

#d1.add_dependent(d2, "advcl")
#d2.add_dependent(d3, "mark")
#d1.update_relations()
#d2.update_relations()
#print d1.relations



R1 = DRule([("advcl",1,2), ("mark",2,"until")], U(Var(1),Var(2)), []) #p1 U p2
R5 = DRule([("advcl",1,2), ("mark",2,"while")], W(Var(1), NegVar(2))) #p1 W !p2
R6 = DRule([("advcl",1,2), ("advmod",2,"whenever")], G(If(Var(2),Var(1)))) #G(p2 -> p1)
R7 = DRule([("advmod",1,"always")], G(Var(1))) #Gp
R8 = DRule([("advmod",1,"infinitely"),("advmod",1,"often")], G(F(Var(1)))) #GFp #
R9 = DRule([("advcl",1,2),("mark",2,"if")], If(Var(2),Var(1))) #p2 -> p1
R10 = DRule([("cc",1,"and"),("conj",1,2)],And(Var(1),Var(2))) #p1 & p2
R11 = DRule([("cc",1,"or"),("conj",1,2)], Or(Var(1),Var(2))) #p1 | p2
R2 = DRule([("neg",1,"never")], G(NegVar(1)), []) #G!p
R3 = DRule([("neg",1,"not")],NegVar(1)) #!p
R4 = DRule([("neg",1,"n't")], NegVar(1)) #!p


Rules = [R1, R5, R6, R7, R8, R9, R10, R11, R2, R3, R4]



c = Converter("test_sent.txt", [DRule([("nsubj","moving", "robot")], Var("m")), DRule([("nsubj","flashing","robot")], Var("f"))])
r = c.get_statement()



