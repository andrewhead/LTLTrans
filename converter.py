from ltl_formula import *
from nltk.corpus import wordnet as wn
import stanfordparser
import re
from nltk.stem import WordNetLemmatizer
import nltk.tokenize 
import nltk.tag
import itertools

wnl = WordNetLemmatizer()

#Helpful function to print dependencies 
def show_deps(sentence):
    if sentence == "I am cool.":
        return "No, you're not."
    s = stanfordparser.parse_sentence(sentence)
    for t in s:
        print t.name, t.governor, t.dependent

#class Replacement:
#    def __init__(self, new_formula = False, next_rules = []):
#        self.formula = new_formula
        #self.rules = next_rules

#node for a dependency tree
class Dnode:
    governor = ""
    dependents = [] #list of 2-tuples containing dependent and relation
    relations = []
    def __init__(self, g, d):
        self.governor = g
        self.dependents = d
        #self.relations = []
    def add_dependent(self, dep, rel):
        self.dependents += [(dep, rel)]
        #self.update_relations() ##BAD FIX THIS
    #finds dnode with governor as given word. returns false, otherwise.
    def find_dnode(self, word): 
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
    def get_relations(self):
        if not self.dependents:
            return set([])
        rel = set()
        for d in self.dependents:
            rel = rel.union( d[0].get_relations() )
            rel = rel.union(set(["(" + d[1] + "," + self.governor + "," + d[0].governor + ")"]))
        #self.relations = list(rel)
        return list(rel)
    def get_trace_from_match(self, replacement, nums_to_words, root_word, rules, index):
        if not nums_to_words:
            return replacement
        trace_map = {}
        print "replacement", replacement, nums_to_words, self
        for i in nums_to_words:
            d = self.find_dnode(nums_to_words[i])
            print i,"dnode",d, d.governor, nums_to_words[i]
            print d.get_relations()
            trace_map[i] = d.apply_rules(rules, index, "trace")
            if not trace_map[i]:
                return False
            print "map:",i, trace_map[i]
        print "map & replacement", trace_map, replacement
        r = re.sub("([0-9])", lambda m: trace_map[int(m.group(1))], replacement)
        print "returning:", r
        trace_map.clear()
        return r
    def get_ltl_from_match(self, replacements, nums_to_words, root_word, rules, index, multi_trans = False, applied_rules = set([])):
        ltl_statements = set()
        if len(nums_to_words) == 0:
            for r in replacements:
                vrbls = r.get_variables() #remove 3 lines once it works
                for v in vrbls:
                    assert(type(v.variable) == str)
                new_ltl = Statement()
                new_ltl.copy(r)
                #print new_ltl
                ltl_statements = ltl_statements.union(set([new_ltl]))
            #print  "1:", list(ltl_statements)
            return list(ltl_statements)
        var_replacements = [[-1]]*(1+ max(nums_to_words)) #will store possible replacements for each variable
        #print nums_to_words, max(nums_to_words)
        #determines ltl statements to replace variables with
        for n in nums_to_words:
            d = self.find_dnode(nums_to_words[n])
            new_ind = 0
            if nums_to_words[n] == root_word:
                new_ind = index
            var_replacements[n] = d.apply_rules(rules, new_ind, "ltl", applied_rules = applied_rules)
        """
        for v in var_replacements:
            for v2 in v:
                if type(v2) != int:
                    v2.print_statement()
        """
        #iterates through all replacement formulas
        for r in replacements:
            #iterates through all combinations of replacements for variables
            for i in itertools.product(*var_replacements):
                new_ltl = Statement()
                new_ltl.copy(r)
                #new_ltl.copy(r.formula)
                variables = new_ltl.get_variables()
                #replaces each integer variable with the chosen ltl_statement
                for v in variables:
                    is_neg = v.is_negative
                    v.copy(i[v.variable])
                    v.is_negative = (v.is_negative != is_neg) #accounts for double-negatives when copying v.variable
                ltl_statements = ltl_statements.union(set([new_ltl]))
        return list(ltl_statements)
        
        
    """
    def get_ltl_from_match(self, replacement, nums_to_words, root_word, rules, index): #takes a matching from variables (ints) to words. Recurses on other rules.
        ltl_node = Statement()
        if (not replacement) or (not replacement.formula):
            return False
        #print str(type(old_ltl_node))
        #print old_ltl_node
        ltl_node.copy(replacement.formula)
        if ltl_node.variable:
            if str(ltl_node.variable).isdigit():
                #print "applying", ltl_node.variable, "to", nums_to_words
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
        #print "left is", ltl_node.left_substatement
        ltl_node.right_substatement = self.get_ltl_from_match(ltl_node.right_substatement, nums_to_words, root_word, rules, index)
        if not ltl_node.right_substatement and not (ltl_node.variable or ltl_node.is_unary):
            return False
        #print "right is", ltl_node.right_substatement 
        return ltl_node
    """
    def apply_rules(self, rules, index = 0, replacement_type = "ltl", multi_translations = False, applied_rules = set([])): #returns full ltl_tree applying rules to dependency_tree
        #print "gov", self.governor
        new_applied_rules = applied_rules
        while index < len(rules):
            matches = rules[index].find_match(self, applied_rules = new_applied_rules) 
            if type(matches) == dict:
                #print "Match found:", matches, rules[index].requirements
                new_applied_rules = new_applied_rules.union(set([rules[index]]))
                if replacement_type == "ltl":
                    return self.get_ltl_from_match(rules[index].replacements, matches, self.governor, rules, index + 1, multi_translations, new_applied_rules)
                elif replacement_type == "trace":
                    return self.get_trace_from_match(rules[index].replacements, matches, self.governor, rules, index + 1)
                else:
                    print "error: please give ltl or trace"
            #print "No match found:", rules[index].requirements
            index += 1
        return []

       

#requirements: list 3-tuples of form (relation, governor, dependent, is_positive)
        #if not is_positive, then the tuple must not appear for the rule to hold
        #any of these may be numbers to represent variables or actual words.
        #1st rule in relation applies to root node of dependency tree
#neg_requirements: like requirements, but the rule cannot apply if any of these patterns are present
#rep: ltl node with numbers (say, n) used to represents slots where get_statement(n) replaces slot in ltl tree 
class DRule(object):
    requirements = []
    replacements = False
    
    def __init__(self, req, rep, neg_rules = set([])):
        self.requirements = []
        #sets negative_rules
        #if any of these rules have occured in the computation, the current rule will not occur. 
        if type(neg_rules) == object:
            self.negative_rules = set([neg_rules])
        elif type(neg_rules) == list:
            self.negative_rules = set(neg_rules)
        elif type(neg_rules) == set:
            self.negative_rules = neg_rules
        else:
            print "incorrect set of negative rules was supplied."
            self.negative_rules = set([])
        for r in req:
            self.add_requirement(r)
        if type(rep) == list:
            self.replacements = rep
        #elif type(rep) == type(Replacement()):
        #    self.replacements = [rep]
        elif type(rep) == type(Statement()) or type(rep) == str:
            self.replacements = [rep]
        else:
            #print rep
            print "Error: please provide valid replacement formula"
    def add_requirement(self, req):
        new_req = [False]*3
        for i in range(0, 3):
            if type(req[i]) == str:
                new_req[i] = [req[i]]
            else: #requirement is variable (int) or list of words
                new_req[i] = req[i]
        if len(req) == 3 or req[3]: #guarantees that negative requirements always come after positive requirements
            self.requirements.append((new_req[0], new_req[1], new_req[2], True))
        else:
            print "negative requirement is given"
            self.requirements = [(new_req[0], new_req[1], new_req[2], False)] + self.requirements
    #helper function to find_match
    def make_regex(self,req, nums_to_words):
        var_assignments = []
        regex = "[(]"
        for r in req[0]:
            regex += r + "|"
        regex = regex[:-1]
        regex += ",("
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
    def find_match(self, dnode, applied_rules = set([])):
        nums_to_words = {}
        if applied_rules.intersection(self.negative_rules):
            return False
        if not self.requirements:
            return False
        #nums_to_words[1] = dnode.governor
        rels = " ".join(dnode.get_relations())
        match_iters = [None]*len(self.requirements)
        changed_words = [[None,None,None] for x in range(0,len(self.requirements))] #Tracks which words were assigned numbers in which position in the requirement-list
        req_itr = 0
        current_match = [[None] for x in range(0,len(self.requirements))]
        root_var = -1
        #print dnode.governor
        #print "rels",rels
        #print "reqs",self.requirements
        if type(self.requirements[0][1]) == int:
            root_var = self.requirements[0][1]
        elif not dnode.governor.split("-")[0] in self.requirements[0][1]: #must match first rule to root of dnode
            #print "HERE",dnode.governor, self.requirements[0][1]
            return False
        while req_itr < len(self.requirements):
            #print req_itr
            #print changed_words
            #print current_match
            req = self.requirements[req_itr]
            #print req
            if req_itr < 0: #It has exhausted all possible matchings. 
                return False
            current_match[req_itr] = None
            changed_words[0][0] = 1
            #print self.requirements
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
            #If there are no possible matches at current dependency-tuple, goes back to last dependency-tuple to find different match
            if not amatch: 
                match_iters[req_itr] = None
                #if not req[3]: #if this is a negative dependency-tuple, there is no possible match (so rule could still apply). Moves to next dep-tuple
#                    req_itr += 1
#                else:
              #     req_itr -= 1
                req_itr -= 1
                continue
            elif (req[1] == root_var and amatch.group(1) != dnode.governor) or (req[2] == root_var and amatch.group(2) != dnode.governor):
                match_iters[req_itr] = m_iter
                continue
            #if amatch and not req[3]: #if a match is found, backtracks (all relevant variables must have been assigned first)
#                match_iters[req_itr] = None
#                req_itr -= 1
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
            
#Rule specific to a variable
class VarRule(DRule):
    def __init__(self, replacements, root, noun = None, prep = None, pobj = None, acomp = None, dobj = None):
        DRule.__init__(self, [], replacements)
        self.root = root
        self.noun = noun
        self.prep = prep
        self.pobl = pobj
        self.requirements = []
        if noun:
            self.add_requirement((["nsubj", "nsubjpass"],root,noun,True))
        if prep:
            self.add_requirement(("prep",root,prep,True))
            if pobj:
                self.add_requirement(("pobj",prep,pobj,True))
        if acomp:
            self.add_requirement(("acomp", root, acomp))
        if dobj:
            self.add_requirement(("dobj", root, dobj))
    def find_match(self,dnode, applied_rules = set([])):
        if self.requirements:
            return DRule.find_match(self,dnode, applied_rules)
        elif self.root == dnode.governor.split("-")[0]: #if we only want to match root up rather than an entire dependency tree
            return {}
        else:
            return None
    
    
    
        


    
class Converter:
    wordmap = {} #maps words to their dependency nodes
    prop_vars = []
    sentence = ""
    
    def __init__(self, sentence, variables, multi_translations = False): 
        self.prop_vars = variables
        self.wordmap = {}
        self.sentence = self.expand_contractions(sentence)
        self.multiple_translations = multi_translations
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
    def expand_contractions(self, sentence):
        new_sentence = re.sub("can't", "cannot", sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("won't", "will not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("isn't", "is not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("it's", "it is", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("aren't", "are not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("wouldn't", "would not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("shouldn't", "should not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("ain't", "is not", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("they're", "they are", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("we're", "we are", new_sentence, flags=re.IGNORECASE)
        new_sentence = re.sub("we'd", "we would", new_sentence, flags=re.IGNORECASE)
        return new_sentence

        
    def add_variable(self, name, description): 
        temp = Converter(description, [])
        amap = DRule([("nsubj",1,2)], False).find_match(temp.wordmap["ROOT-0"])
        if amap:
            self.prop_vars.append(DRule([("nsubj",str(amap[1].split("-")[0]),str(amap[2].split("-")[0]))], Var(name)))
    def get_statement(self, replacement_type = "ltl"): #Returns the LTL statement corresponding to the given English sentence
        current_statements = []
        for d in self.wordmap["ROOT-0"].dependents:
            if replacement_type == "ltl":
                ltl_statements = d[0].apply_rules(LTL_Rules + self.prop_vars, 0, "ltl", multi_translations = self.multiple_translations)
            elif replacement_type == "trace":
                ltl_statements = d[0].apply_rules(Trace_Rules + self.prop_vars, 0, "trace", multi_translations = self.multiple_translations)
            else:
                print "please input a valid conversion type (ltl, trace)"
                return "error"
            if not ltl_statements:
                continue
            if current_statements:
                new_statements = []
                for p in itertools.product(*[current_statement, ltl_statements]):
                    print "p is", p
                    new_statements.append(And(p[0], p[1]))
                current_statements = new_statements
            else:
                current_statements = ltl_statements
        return current_statements
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
    def lemmatize_relations(self, relations, pos_map): #Replaces words in relations with lemmatized version (removes tense and pluralization)
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


R30 = DRule([("prep", 1, ["at", "in", "during","for"]),
             ("amod", ["moment","step","point","second", "time"], ["first", "initial"]),
             ("pobj", ["at","in","during","for"], ["moment","step","point","second", "time"])],
            Var(1))
R31 = DRule([("advmod", 1, ["initially", "currently", "now"])], Var(1))
R1 = DRule([("advcl",1,2), ("mark",2,"until")], U(Var(1),Var(2))) #p1 U p2
R14 = DRule([("advcl",1,2), ("mark", 2, "unless")], Iff(Var(2), NegVar(1))) #p2 -> ~p1
R5 = DRule([("advcl",1,2), ("mark",2,"while")], W(Var(1), NegVar(2))) #p1 W !p2
R6 = DRule([("advcl",1,2), ("advmod",2,"whenever")], G(If(Var(2),Var(1)))) #G(p2 -> p1)
R17 = DRule([("prep", 1, ["at", "in", "during","for"]),
             ("det", ["moment","step","point","second", "time", "frame"], ["every", "all", "any"]),
             ("pobj", ["at","in","during", "for"], ["moment","step","point","second","time", "frame"])],
            G(Var(1)))
R21 = DRule([("ccomp","case",1),("advmod","case","always")], G(Var(1)))
R22 = DRule([("ccomp","case",1),("neg","case","never")], G(NegVar(1)))
R23 = DRule([("ccomp","case",1),("advmod","case", ["always", "sometimes"])], F(Var(1)))
R18 = DRule([("prep", 1, ["at", "in", "during","for"]),
             ("det", ["moment","step","point","second", "time", "frame"], "some"),
             ("pobj", ["at","in","during","for"], ["moment","step","point","second", "time", "frame"])],
            F(Var(1)))
#R24 = DRule([("aux", 1, "will"),("advmod", 1, "eventually", False)], [Var(1), F(Var(1))])
R8 = DRule([("advmod",1,"infinitely"),("advmod",1,"often")], G(F(Var(1)))) #GFp #

R29 = DRule([("advcl",1,2),("mark",2,["if","when"]),("advmod",2,"now")], If(Var(2), Var(1)))
R9 = DRule([("advcl",1,2),("mark",2, "if")], [If(Var(2),Var(1)), G(If(Var(2),Var(1)))], [R17, R21, R22, R23, R29, R30, R31]) #p2 -> p1, or G(p2 -> p1)
R28 = DRule([("advcl",1,2),("mark",2,["if", "when"])], If(Var(2),Var(1)), [R9, R29])
#R24 = DRule([("aux", 1, "will")], [Var(1), F(Var(1))])
R7 = DRule([("advmod",1,"eventually")], F(Var(1))) #Gp
R4 = DRule([("advmod",1,"always")], G(Var(1))) #Gp
R10 = DRule([("cc",1,"and"),("conj",1,2)],And(Var(1),Var(2))) #p1 & p2
R11 = DRule([("cc",1,"or"),("conj",1,2)], Or(Var(1),Var(2))) #p1 | p2
R19 = DRule([("prep", 1, ["at", "in", "during", "for"]),
             ("amod", ["moment","step","point","second", "time", "frame"], ["next", "following"]),
             ("pobj", ["at","in","during", "for"], ["moment","step","point","second", "time", "frame"])],
            X(Var(1)))
R12 = DRule([("advmod", 1, "next")], X(Var(1)))
R15 = DRule([("parataxis", 1, 2), ("advmod", 2, "then")], And(Var(1),X(Var(2)))) # p1 & Xp2
R16 = DRule([("ccomp", 1, 2), ("advmod", 2, "then")], And(Var(1), X(Var(2)))) #possibly a mistake in SP
R20 = DRule([("xcomp", "stop", 1)], NegVar(1))
R32 = DRule([("dobj",1,["time"]), ("predet",["time"],"all")], G(Var(1))) ###ADD STUFFFFF
R2 = DRule([("neg",1,"never")], G(NegVar(1))) #G!p
R3 = DRule([("neg",1,["not","n't"])],NegVar(1)) #!p
R27 = DRule([("aux", 1, "will")], [F(Var(1)), Var(1)], [R4, R7, R8, R18, R21, R22, R14, R1, R2, R30, R31])
R25 = DRule([("ccomp", "true", 1)], Var(1))
R26 = DRule([("ccomp", "false", 1)], NegVar(1))

#Problem: The robot never stops killing.

#Tests
s1 = "The robot is moving until the light is flashing." #m U f
s2 = "The robot moves while the light is not flashing." #m W f
s3 = "The robot moves, unless the light is flashing." # f -> ~m


LTL_Rules = [R30, R31, R1, R14, R5, R6, R21, R22, R23, R8, R17, R29, R9, R28, R7, R4, R10, R11, R12, R15, R16, R18, R19, R20, R32, R2, R3, R27, R25, R26]

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
    """
    while True:
        var = raw_input("Define a variable as 'name: description': ")
        if var == "done":
            break
        m = var.split(":")
        m[1]= m[1].strip()
        print m[0],m[1]d
        c.add_variable(m[0],m[1])
    for p in c.prop_vars:
        print "k",p.requirements
    print "prop_Vars", c.prop_vars
    """
   # c.prop_vars = [DRule([("nsubj","move",0)],Var("m")),DRule([("nsubj","flash",0)],Var("f"))]
    c.prop_vars = [VarRule(Var("c"),"chew"), VarRule(Var("k"),"kick")]
    r = c.get_statement()
    if r:
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
#r = R2.find_match(c.wordmap["ROOT-0"].dependents[0][0])


########## TRACES ###############
V1 = DRule([("nsubj","flip","switch")], "f")
V2 = DRule([("nsubj", "move", "robot")], "b")

Trace_Rules = [
    DRule([("parataxis",4,2)], "42"),
    DRule([("advmod",1,"twice")], "11"),
    DRule([("tmod",1,"time"),("num","time","two")], "11"),
    DRule([("tmod",1,"time"),("num","time","three")], "111"),
    DRule([("tmod",1,"time"),("num","time","four")], "1111"),
    DRule([("dobj",1,"time"),("num","time","two")], "11"), #This may be a fault in the stanford parser
    DRule([("dobj",1,"time"),("num","time","three")], "111"),
    DRule([("dobj",1,"time"),("num","time","four")], "1111"),
    DRule([("prep",1,"for"),("pobj", "for", "step"),("num", "step", "two")], "11"),
    DRule([("advmod",1,["repeatedly", "continuously"])], "(1)w"),
    DRule([("neg", 1, ["not","n't"])], "~1")
    ]
"""
print "A"
VAR = VarRule(Var("m"), "move", noun = "robot")
c = Converter("The robot will move.", [VAR], LTL_Rules)
r = c.get_statement()
print "Translations:"
for a in r:
    a.print_statement()
    print ""
"""
#class TraceRule(DRule):
#    pass

#class TraceConverter(Converter):
 #   def get_trace
            
def print_ltl(ltl_statements):
    if not ltl_statements:
        print "No translations"
    print "Translations: "
    for l in ltl_statements:
        l.print_statement()
        print ""


