package com.headstrong.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;


public class LtlExplainer {

    private Lexicon lexicon = Lexicon.getDefaultLexicon();
    private NLGFactory nlgFactory = new NLGFactory(lexicon);
    private Realiser realiser = new Realiser(lexicon);
    private List<Object> propositions;
    private int mDepth = 0;

    public enum NodeType {
        PROPVAR,
        GLOBAL,
        FUTURE,
        NOT_FUTURE,
        GLOBAL_FUTURE,
        NEXT,
        OR,
        AND,
        IMPLIES,
        UNTIL,
        NOT,
    };
    public ArrayList<NodeType> tempUnaries = new ArrayList<NodeType>();  // initialied in ctor

    public LtlExplainer(List<Object> propositions) {
        this.propositions = propositions;
        this.tempUnaries.add(NodeType.GLOBAL);
        this.tempUnaries.add(NodeType.FUTURE);
        this.tempUnaries.add(NodeType.GLOBAL_FUTURE);
        this.tempUnaries.add(NodeType.NOT_FUTURE);
    }

    public NodeType getNodeType(Object o) {
        NodeType nt = null;
        if (o instanceof String) {
            nt = NodeType.PROPVAR;
        } else {
            Map m = (Map) o;
            if (m.containsKey("binop")) {
                Map opM = (Map) m.get("binop");
                String opType = (String) opM.get("type");
                if (opType.equals("and")) nt = NodeType.AND;
                if (opType.equals("or")) nt = NodeType.OR;
                else if (opType.equals("implies")) nt = NodeType.IMPLIES;
                else if (opType.equals("until")) nt = NodeType.UNTIL;
            } else if (m.containsKey("unop")) {
                Map opM = (Map) m.get("unop");
                String opType = (String) opM.get("type");
                NodeType argType = getNodeType(opM.get("arg"));
                if (opType.equals("not")) {
                    if (argType == NodeType.FUTURE) nt = NodeType.NOT_FUTURE;
                    else nt = NodeType.NOT;
                } else if (opType.equals("global")) {
                    if (argType == NodeType.FUTURE) nt = NodeType.GLOBAL_FUTURE;
                    else nt = NodeType.GLOBAL;
                }
                else if (opType.equals("future")) nt = NodeType.FUTURE;
                else if (opType.equals("next")) nt = NodeType.NEXT;
            }
        }
        return nt;
    }

    public NLGElement visit(Object n) {
        this.mDepth += 1;
        NLGElement result = null;
        NodeType type = getNodeType(n);
        if (type == NodeType.PROPVAR) result = this.visitProposition(n);
        else if (type == NodeType.NOT) result = this.visitNot(n);
        else if (type == NodeType.GLOBAL) result = this.visitGlobal(n);
        else if (type == NodeType.FUTURE) result = this.visitFuture(n);
        else if (type == NodeType.NOT_FUTURE) result = this.visitNotFuture(n);
        else if (type == NodeType.GLOBAL_FUTURE) result = this.visitGlobalFuture(n);
        else if (type == NodeType.UNTIL) result = this.visitUntil(n);
        else if (type == NodeType.NEXT) result = this.visitNext(n);
        else if (type == NodeType.AND) result = this.visitAnd(n);
        else if (type == NodeType.OR) result = this.visitOr(n);
        else if (type == NodeType.IMPLIES) result = this.visitImplies(n);
        if (this.mDepth == 1 && !this.tempUnaries.contains(type)) {
            this.addFrontModifier(result, "currently,");
        }
        this.mDepth -= 1;
        return result;
    }

    private NLGElement visitProposition(Object n) {
        int index = Integer.parseInt((String)n) - 1;
        Map prop = (Map) this.propositions.get(index);
        SPhraseSpec clause = this.nlgFactory.createClause();
        NPPhraseSpec subjPhrase = this.nlgFactory.createNounPhrase(prop.get("subject"));
        clause.setSubject(subjPhrase);
        clause.setVerb(prop.get("verb"));
        // The object is optional for our propositions
        if (prop.containsKey("object")) {
            NPPhraseSpec objPhrase = this.nlgFactory.createNounPhrase(prop.get("object"));
            clause.setObject(objPhrase);
        }
        return clause;
    }

    private NLGElement visitNot(Object nn) {
        Map m = (Map) nn;
        Map op = (Map) m.get("unop");
        NLGElement clause = this.visit(op.get("arg"));
        System.out.println(clause);
        if (clause instanceof PhraseElement) {
            clause.setFeature(Feature.NEGATED, ! (Boolean) (clause.getFeature(Feature.NEGATED)));
        } else {
            this.addFrontModifier(clause, "it is not the case that");
        }
        return clause;
    }

    private NLGElement visitNext(Object nn) {
        Map m = (Map) nn;
        Map op = (Map) m.get("unop");
        NLGElement child = this.visit(op.get("arg"));
        NLGElement advPhrase = this.nlgFactory.createAdverbPhrase("in the next step");
        this.addComplement(child, advPhrase);
        // child.setFeature(Feature.TENSE, Tense.FUTURE);
        return child;
    }

    private NLGElement visitGlobal(Object gn) {
        Map m = (Map) gn;
        Map op = (Map) m.get("unop");
        NLGElement child = this.visit(op.get("arg"));
        // If this is the root of the tree, then we believe that the
        // global "always" behavior is implied, so we don't add the modifier.
        if (this.mDepth > 1) {
            this.addFrontModifier(child, "it's always the case that");
        }
        return child;
    }

    private NLGElement visitFuture(Object fn) {
        Map m = (Map) fn;
        Map op = (Map) m.get("unop");
        NLGElement child = this.visit(op.get("arg"));
        this.addFrontModifier(child, "at some point it will be the case that");
        return child;
    }

    private NLGElement visitNotFuture(Object nfn) {
        Map m = (Map) nfn;
        Map nop = (Map) m.get("unop");
        Map arg = (Map) nop.get("arg");
        Map fop = (Map) arg.get("unop");
        NLGElement child = this.visit(fop.get("arg"));
        this.addFrontModifier(child, "at no point in the future will it be that");
        return child;
    }

    private NLGElement visitGlobalFuture(Object gfn) {
        Map m = (Map) gfn;
        Map gop = (Map) m.get("unop");
        Map arg = (Map) gop.get("arg");
        Map fop = (Map) arg.get("unop");
        NLGElement child = this.visit(fop.get("arg"));
        child.setFeature(Feature.TENSE, Tense.FUTURE);
        NLGElement advPhrase = this.nlgFactory.createAdverbPhrase("infinitely often in the future");
        this.addComplement(child, advPhrase);
        return child;
    }

    private NLGElement visitAnd(Object an) {
        Map m = (Map) an;
        Map op = (Map) m.get("binop");
        NLGElement clause1 = this.visit(op.get("arg1"));
        NLGElement clause2 = this.visit(op.get("arg2"));
        CoordinatedPhraseElement coord = nlgFactory.createCoordinatedPhrase();
        coord.addCoordinate(clause1);
        coord.addCoordinate(clause2);
        return coord;
    }

    private NLGElement visitOr(Object on) {
        Map m = (Map) on;
        Map op = (Map) m.get("binop");
        NLGElement clause1 = this.visit(op.get("arg1"));
        NLGElement clause2 = this.visit(op.get("arg2"));
        CoordinatedPhraseElement coord = nlgFactory.createCoordinatedPhrase();
        coord.setFeature(Feature.CONJUNCTION, "or");
        coord.addCoordinate(clause1);
        coord.addCoordinate(clause2);
        return coord;
    }

    private NLGElement visitImplies(Object in) {
        Map m = (Map) in;
        Map op = (Map) m.get("binop");
        NLGElement child0 = this.visit(op.get("arg1"));
        NLGElement child1 = this.visit(op.get("arg2"));
        this.addFrontModifier(child0, "if");
        this.addFrontModifier(child1, "then");
        this.addComplement(child0, child1);
        return child0;
    }

    private NLGElement visitUntil(Object un) {
        Map m = (Map) un;
        Map op = (Map) m.get("binop");
        NLGElement child0 = this.visit(op.get("arg1"));
        NLGElement child1 = this.visit(op.get("arg2"));
        CoordinatedPhraseElement coord = nlgFactory.createCoordinatedPhrase();
        this.addFrontModifier(child1, "until");
        this.addComplement(child0, child1);
        return child0;
    }

    private NLGElement addFrontModifier(NLGElement nlge, String fm) {
        StringElement fme = new StringElement(fm);
        NLGElement leftChild = nlge;
        while (leftChild != null) {
            if (leftChild instanceof PhraseElement) {
                PhraseElement pe = (PhraseElement)leftChild;
                List<NLGElement> fms = pe.getFrontModifiers();
                pe.setFrontModifier(fme);
                for (NLGElement oldFm:fms) {
                    pe.addFrontModifier(oldFm);
                }
                break;
            }
            leftChild = nlge.getChildren().get(0);
        }
        return nlge;
    }

    private NLGElement addComplement(NLGElement e1, NLGElement e2) {
        if (e1 instanceof PhraseElement) {
            ((PhraseElement)e1).addComplement(e2);
        } else if (e1 instanceof CoordinatedPhraseElement) {
            ((CoordinatedPhraseElement)e1).addComplement(e2);
        }
        // Override the 'that' complement that is added to the second phrase by SimpleNLG
        e2.setFeature(Feature.COMPLEMENTISER, "");
        return e1;
    }

    public String render(Object formula) {
        this.mDepth = 0;
        NLGElement clause = this.visit(formula);
        return realiser.realiseSentence(clause);
    }

}
