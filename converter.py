from ltl_formula import *
import stanfordparser
import re
from nltk.stem import WordNetLemmatizer
import nltk.tokenize 
import nltk.tag 

wnl = WordNetLemmatizer()

def show_deps(sentence):
    s = stanfordparser.parse_sentence(sentence)
    for t in s:
        print t.name, t.governor, t.dependent
        

#node for a dependency tree
class Dnode:
    governor = ""
    dependents = [] #list of 2-tuples containing dependent and relation
    relations = []
    def __init__(self, g, d):
        self.governor = g
        self.dependents = d
        self.relations = []
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
    def update_relations(self):
        if not self.dependents:
            return set([])
        rel = set()
        for d in self.dependents:
            rel = rel.union( d[0].update_relations() )
            rel = rel.union(set(["(" + d[1] + "," + self.governor + "," + d[0].governor + ")"]))
        self.relations = list(rel)
        return rel
    def get_ltl_from_match(self, old_ltl_node, nums_to_words, root_word, rules, index):
        ltl_node = Statement()
        if not old_ltl_node:
            return False
        print str(type(old_ltl_node))
        print old_ltl_node
        ltl_node.copy(old_ltl_node)
        if ltl_node.variable:
            if str(ltl_node.variable).isdigit():
                print "applying", ltl_node.variable, "to", nums_to_words
                if ltl_node.variable in nums_to_words:
                    new_ind = 0
                    new_root = nums_to_words[ltl_node.variable]
                    if new_root == root_word:
                        new_ind = index
                    d = self.find_dnode(new_root)
                    if not d:
                        print "Error:", new_root, "not in tree with", self.governor, "as root"
                        return False
                    temp = d.apply_rules(rules, new_ind)
                    if not temp:
                        print "Error: no match found after index", new_ind, "for dependency tree with", self.governor, "as root"
                        return False
                    print temp, new_ind
                    print temp.is_negative, ltl_node.is_negative, self.governor
                    temp.is_negative = (temp.is_negative != ltl_node.is_negative)
                    return temp
                else:
                    print "Error: variable " + str(ltl_node.variable), "not in current match"
                    return False
            else:
                return ltl_node
        ltl_node.left_substatement = self.get_ltl_from_match(ltl_node.left_substatement, nums_to_words, root_word, rules, index)
        if not ltl_node.left_substatement and not ltl_node.variable:
            return False
        print "left is", ltl_node.left_substatement
        ltl_node.right_substatement = self.get_ltl_from_match(ltl_node.right_substatement, nums_to_words, root_word, rules, index)
        if not ltl_node.right_substatement and not (ltl_node.variable or ltl_node.is_unary):
            return False
        print "right is", ltl_node.right_substatement 
        return ltl_node

    def apply_rules(self, rules, index = 0): #returns full ltl_tree applying rules to dependency_tree
        #print "gov", self.governor
        while index < len(rules):
            matches = rules[index].find_match2(self)
            if type(matches) == dict:
                print "Match found:", matches, rules[index].requirements
                print self.governor
                return self.get_ltl_from_match(rules[index].replacement, matches, self.governor, rules, index + 1)
            #print "No match found:", rules[index].requirements
            index += 1
        return False
        

#requirements: list 3-tuples of form (relation, governor, dependent, is_positive)
        #if not is_positive, then the tuple must not appear for the rule to hold
        #any of these may be numbers to represent variables or actual words.
        #1st rule in relation applies to root node of dependency tree
#neg_requirements: like requirements, but the rule cannot apply if any of these patterns are present
#rep: ltl node with numbers (say, n) used to represents slots where get_statement(n) replaces slot in ltl tree 
class DRule(object):
    requirements = []
    #neg_requirements = []
    #regex_patterns = list()
    replacement = False
    def __init__(self, req, rep):
        self.requirements = []
        for r in req:
            self.add_requirement(r)
        self.replacement = rep
    def add_requirement(self, req):
        if type(req[1]) == str:
            r1 = [req[1]]
        else:
            r1 = req[1]
        if type(req[2]) == str:
            r2 = [req[2]]
        else:
            r2 = req[2]
        if len(req) == 3 or req[3]: #guarantees that negative requirements always come after positive requirements
            self.requirements.append((req[0], r1, r2, True))
        else:
            self.requirements = [(req[0],r1,r2,False)] + self.requirements
        
        """
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
        """
    """
    def find_match(self, dnode):
        #print "finding match for", dnode.governor, "with", self.requirements
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
    """
    #helper function to find_match
    def make_regex(self,req, nums_to_words):
        var_assignments = []
        regex = "[(]" + req[0] + ",("
        if type(req[1]) == int:
            if req[1] in nums_to_words:
                regex += nums_to_words[req[1]]
            else:
                regex += "[a-zA-Z]+-[0-9]+"
        else:
            for r in req[1]:
                regex += r + "-[0-9]+|"
            regex = regex[:-1]
        regex += "),("
        if type(req[2]) == int:
            if req[2] in nums_to_words:
                regex += nums_to_words[req[2]]
            else:
                regex += "[a-zA-Z]+-[0-9]+"
        else:
            for r in req[2]:
                regex += r + "-[0-9]+|"
            regex = regex[:-1]
        regex += ")[)]"
        return regex
    def find_match2(self,dnode):
        nums_to_words = {}
        #nums_to_words[1] = dnode.governor
        rels = " ".join(dnode.relations)
        match_iters = [None]*len(self.requirements)
        changed_words = [[None,None,None] for x in range(0,len(self.requirements))] #Tracks which words were assigned numbers in which position in the requirement-list
        req_itr = 0
        current_match = [[None] for x in range(0,len(self.requirements))]
        while req_itr < len(self.requirements):
            req = self.requirements[req_itr]
            if req_itr < 0: #It has exhausted all possible matchings. 
                return False
            current_match[req_itr] = None
            changed_words[0][0] = 1
            #print changed_words, req[1], nums_to_words
            if changed_words[req_itr][1]:
                del nums_to_words[req[1]]
            if changed_words[req_itr][2]:
                del nums_to_words[req[2]]
            amatch = None
            m_iter = None
            if not match_iters[req_itr]: #If loop is starting on a new dependency-tuple, finds all tuples in rels which match the rule.
                regex = self.make_regex(req, nums_to_words)
                m_iter = re.finditer(regex, rels, flags=re.IGNORECASE)
                amatch = next(m_iter, None)
            else:
                m_iter = match_iters[req_itr]
                amatch = next(m_iter, None)
            if not amatch: #If there are no possible matches at current dependency-tuple, goes back to last dependency-tuple to find different match
                match_iters[req_itr] = None
                if not req[3]: #if this is a negative dependency-tuple, there is no possible match (so rule could still apply). Moves to next dep-tuple
                    req_itr += 1
                else:
                    req_itr -= 1
                continue
            if amatch and not req[3]: #if a match is found, backtracks (all relevant variables must have been assigned first)
                match_iters[req_itr] = None
                req_itr -= 1
            match_iters[req_itr] = m_iter                
            if req[1] != 0 and type(req[1]) == int and not req[1] in nums_to_words:
                changed_words[req_itr][1] = amatch.group(1)
                nums_to_words[req[1]] = amatch.group(1) 
            if req[2] != 0 and type(req[2]) == int and not req[2] in nums_to_words:
                changed_words[req_itr][2] = amatch.group(2)
                nums_to_words[req[2]] = amatch.group(2)
            current_match[req_itr] = amatch
            req_itr += 1
        #print current_match
        return nums_to_words
        #return [c.group() for c in current_match]
            
                    
#class VarRule(DRule):
#    def __init__(self, node, req, rep)
#    ltl_node = None
    
    
        
                        
            

    
class Converter:
    wordmap = {} #maps words to their dependency nodes
    prop_vars = []
    sentence = ""
    def __init__(self, sentence, variables):
        self.prop_vars = variables
        self.wordmap = {}
        self.sentence = sentence
        relations = stanfordparser.parse_sentence(sentence)

        #assembles part of speech map
        pos_map = {}
        tokenized = nltk.word_tokenize(sentence)
        sent_pos = nltk.pos_tag(tokenized)
        ind = 1
        for word in sent_pos:
            pos_map[word[0] + "-" + str(ind)] = word[1]
            ind += 1
        relations = self.lemmatize_relations(relations, pos_map)
        self.sentence = sentence
        t = []
        for r in relations:
            l = r
            t += [l]
            if not l.governor in self.wordmap:
                self.wordmap[l.governor] = Dnode(l.governor, [])
            if not l.dependent in self.wordmap:
                self.wordmap[l.dependent] = Dnode(l.dependent, [])
        self.wordmap["ROOT-0"] = Dnode("ROOT-0",[])
        for l in t:
            #print "adding:", l[1], l[2], l[0]
            self.wordmap[l.governor].add_dependent(self.wordmap[l.dependent], l.name)
        
    def add_variable(self, name, description):
        temp = Converter(description, [])
        amap = DRule([("nsubj",1,2)], False).find_match2(temp.wordmap["ROOT-0"])
        if amap:
            self.prop_vars.append(DRule([("nsubj",str(amap[1].split("-")[0]),str(amap[2].split("-")[0]))], Var(name)))
            
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
    #Determines the type (noun,verb,adjective,or adverb) for a given word, based on its part-of-speech tag
    def get_word_type(self, pos_tag):
        if pos_tag in ["NN", "NNS", "NNP", "NNPS"]:
            return "n"
        elif pos_tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            return "v"
        elif pos_tag in  ['RB', 'RBR', 'RBS']:
            return "r"
        elif pos_tag in ['JJ', 'JJR', 'JJS']:
            return "a"
        else:
            #print "Part of Speech", pos_tag, "not recognized"
            return "n"
    def lemmatize_relations(self, relations, pos_map):
        new_rels = []
        for r in relations:
            new_gov = ""
            if r.name == "root":
                new_gov = "ROOT-0"
            else:
                new_gov = wnl.lemmatize(r.governor.split("-")[0], pos = self.get_word_type(pos_map[r.governor])).lower()+"-"+r.governor.split("-")[1]
            new_dep = wnl.lemmatize(r.dependent.split("-")[0], pos = self.get_word_type(pos_map[r.dependent])).lower()+"-"+r.dependent.split("-")[1]
            new_rels.append(stanfordparser.TypedDependency(r.name, new_gov, new_dep))
        return new_rels
            
"""
    def lemmatize_dependencies(dependencies): #list of (name, governor, dependency))
        pos_map = {}
        for d in dependencies:
            gov_type = "n"
            dep_type = "n"
            if d[0] == "nsubj" or "mark" or "neg" or "advmod" :
                gov_type = "v"
            elif d[0] == "advcl":
                gov_type = "v"
                dep_type = "v"
        return (dependency[0], wnl.lemmatize
"""
#d1 = Dnode("moves-1", [])
#d2 = Dnode("improves-2",[])
#d3 = Dnode("until-3",[])

#d1.add_dependent(d2, "advcl")
#d2.add_dependent(d3, "mark")
#d1.update_relations()
#d2.update_relations()
#print d1.relations



R1 = DRule([("advcl",1,2), ("mark",2,"until")], U(Var(1),Var(2))) #p1 U p2
R14 = DRule([("advcl",1,2), ("mark", 2, "unless")], If(Var(2), NegVar(1))) #p2 -> ~p1
R5 = DRule([("advcl",1,2), ("mark",2,"while")], W(Var(1), NegVar(2))) #p1 W !p2
R6 = DRule([("advcl",1,2), ("advmod",2,"whenever")], G(If(Var(2),Var(1)))) #G(p2 -> p1)
R4 = DRule([("advmod",1,"always")], G(Var(1))) #Gp
R17 = DRule([("prep", 1, ["at", "in", "during"]),
             ("det", ["moment","step","point","second"], ["every", "all"]),
             ("pobj", ["at","in","during"], ["moment","step","point","second"])],
            G(Var(1)))
R18 = DRule([("prep", 1, ["at", "in", "during"]),
             ("det", ["moment","step","point","second"], "some"),
             ("pobj", ["at","in","during"], ["moment","step","point","second"])],
            F(Var(1)))
R21 = DRule([("aux",1,"will"),("advcl",1,2),("mark",2,"until",False)],F(Var(1)))
R22 = DRule([("aux",1,"will"),("advcl",1,2,False)], F(Var(1)))
R7 = DRule([("advmod",1,"eventually")], F(Var(1))) #Gp
R8 = DRule([("advmod",1,"infinitely"),("advmod",1,"often")], G(F(Var(1)))) #GFp #

R9 = DRule([("advcl",1,2),("mark",2,"if")], If(Var(2),Var(1))) #p2 -> p1
R10 = DRule([("cc",1,"and"),("conj",1,2)],And(Var(1),Var(2))) #p1 & p2
R11 = DRule([("cc",1,"or"),("conj",1,2)], Or(Var(1),Var(2))) #p1 | p2
R19 = DRule([("prep", 1, ["at", "in", "during"]),
             ("amod", ["moment","step","point","second"], ["next", "following"]),
             ("pobj", ["at","in","during"], ["moment","step","point","second"])],
            X(Var(1)))
R12 = DRule([("advmod", 1, "next")], X(Var(1)))
R15 = DRule([("parataxis", 1, 2), ("advmod", 2, "then")], And(Var(1),X(Var(2)))) # p1 & Xp2
R16 = DRule([("ccomp", 1, 2), ("advmod", 2, "then")], And(Var(1), X(Var(2)))) #possibly a mistake in SP
R20 = DRule([("xcomp", "stop", 1)], NegVar(1))
R2 = DRule([("neg",1,"never")], G(NegVar(1))) #G!p
R3 = DRule([("neg",1,["not","n't"])],NegVar(1)) #!p

#Problem: The robot never stops killing.

#Tests
s1 = "The robot is moving until the light is flashing." #m U f
s2 = "The robot moves while the light is not flashing." #m W f
s3 = "The robot moves, unless the light is flashing." # f -> ~m


Rules = [R1, R14, R5, R6, R4, R21, R22, R7, R8, R9, R10, R11, R12, R15, R16, R17, R18, R19, R20, R2, R3]

"""
sentence = raw_input("What would you like to parse?: ")
variables = []
while True:
    var = raw_input("Define a variable as 'type,governor,dependent': ")
    print var
    if var == "done":
        break
    m = var.split(",")
    var_name = raw_input("name this variable: ")
    print m[0],m[1],m[2]
    variables += [DRule([(m[0], m[1], m[2])], Var(var_name))]
#print variables
#c = Converter(sentence, variables)
"""

def run(sentence = "If the robot kills, it loves"):
    #sentence = raw_input("What would you like to parse?: ")
    #print sentence
    variables = []
    c = Converter(sentence, [])
    print c.wordmap
    """
    while True:
        var = raw_input("Define a variable as 'name: description': ")
        if var == "done":
            break
        m = var.split(":")
        m[1]= m[1].strip()
        print m[0],m[1]
        c.add_variable(m[0],m[1])
    for p in c.prop_vars:
        print "k",p.requirements
    print "prop_Vars", c.prop_vars
    """
    c.prop_vars = [DRule([("nsubj","move",0)],Var("m")),DRule([("nsubj","flash",0)],Var("f"))]
    r = c.get_statement()
    if r:
        print r.left_substatement, r.right_substatement, r.operator
        print sentence, " ---> ",
        r.print_statement()
        t = Statement()
        t.copy(r)
        return t
    else:
        print "No valid translation"

#c = Converter("The robot never kills.", [DRule([("nsubj","kills","robot")],Var("k"))])
#r = c.get_statement()
#r.print_statement()

#c = Converter("The robot never moves", [])
#print c.wordmap["ROOT-0"].dependents[0][0]
#r = R2.find_match2(c.wordmap["ROOT-0"].dependents[0][0])


