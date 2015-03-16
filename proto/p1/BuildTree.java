import java.util.ArrayList;
import java.util.List;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;


public class BuildTree {

    private static class Node {
        public ArrayList<Node> children = new ArrayList<Node>();
    }

    private static class ClauseBuilderVisitor {

        public NLGFactory nlgFactory;

        public ClauseBuilderVisitor(NLGFactory nlgFactory) {
            this.nlgFactory = nlgFactory;
        }

        public NLGElement visit(Node n) {
            if (n instanceof PropositionNode) {
                return this.visitProposition((PropositionNode)n);
            } else if (n instanceof NotNode) {
                return this.visitNot((NotNode) n);
            } else if (n instanceof NextNode) {
                return this.visitNext((NextNode) n);
            } else if (n instanceof GlobalNode) {
                return this.visitGlobal((GlobalNode) n);
            } else if (n instanceof AndNode) {
                return this.visitAnd((AndNode) n);
            } else if (n instanceof ImpliesNode) {
                return this.visitImplies((ImpliesNode) n);
            } else {
                return null;
            }
        }

        private NLGElement visitProposition(PropositionNode pn) {
            NPPhraseSpec subjPhrase = this.nlgFactory.createNounPhrase(pn.subject);
            NPPhraseSpec objPhrase = this.nlgFactory.createNounPhrase(pn.object);
            SPhraseSpec clause = this.nlgFactory.createClause();
            clause.setSubject(subjPhrase);
            clause.setVerb("be");
            clause.setObject(objPhrase);
            return clause;
        }

        private NLGElement visitNot(NotNode nn) {
            NLGElement clause = this.visit(nn.children.get(0));
            clause.setFeature(Feature.NEGATED, ! (Boolean) (clause.getFeature(Feature.NEGATED)));
            return clause;
        }

        private NLGElement visitNext(NextNode nn) {
            NLGElement child = this.visit(nn.children.get(0));
            // TODO enable user-customized timing, and squashing of next
            PPPhraseSpec prepPhrase = this.nlgFactory.createPrepositionPhrase("in", "1 second");
            this.addComplement(child, prepPhrase);
            child.setFeature(Feature.TENSE, Tense.FUTURE);
            return child;
        }

        /**
         *  Add front modifier to _start_ of a phrase element's front modifiers.
         */
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

        /**
         *  Utility function for adding complements to phrase elements and coordinated phrase elements.
         */
        private NLGElement addComplement(NLGElement e1, NLGElement e2) {
            if (e1 instanceof PhraseElement) {
                ((PhraseElement)e1).addComplement(e2);
            } else if (e1 instanceof CoordinatedPhraseElement) {
                ((CoordinatedPhraseElement)e1).addComplement(e2);
            }
            return e1;
        }

        private NLGElement visitGlobal(GlobalNode gn) {
            NLGElement child = this.visit(gn.children.get(0));
            this.addFrontModifier(child, "It always holds that");
            return child;
        }

        private NLGElement visitAnd(AndNode an) {
            NLGElement clause1 = this.visit(an.children.get(0));
            NLGElement clause2 = this.visit(an.children.get(1));
            CoordinatedPhraseElement coord = nlgFactory.createCoordinatedPhrase();
            coord.addCoordinate(clause1);
            coord.addCoordinate(clause2);
            return coord;
        }

        private NLGElement visitImplies(ImpliesNode in) {
            NLGElement child0 = this.visit(in.children.get(0));
            NLGElement child1 = this.visit(in.children.get(1));
            this.addFrontModifier(child1, "then");
            this.addFrontModifier(child0, "if");
            this.addComplement(child0, child1);
            return child0;
        }

    }

    /* Unary operators */
    private static class NotNode extends Node {}
    private static class NextNode extends Node {}
    private static class GlobalNode extends Node {}

    /* Binary operators */
    private static class AndNode extends Node {}
    private static class ImpliesNode extends Node {}

    /* Propositions */
    private static class PropositionNode extends Node {
       
        public String subject;
        public String object;

        public PropositionNode(String subject, String object) {
            this.subject = subject;
            this.object = object;
        }

    }

    public static void main(String[] args) {
        
        // Initialize SimpleNLG components
        Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        // Build our tree
        PropositionNode node = new PropositionNode("the door", "closed");
        PropositionNode node2 = new PropositionNode("the door", "closed");
        NotNode nn = new NotNode();
        nn.children.add(node2);
        NextNode nxn = new NextNode();
        nxn.children.add(nn);
        AndNode an = new AndNode();
        an.children.add(node);
        an.children.add(nxn);
        PropositionNode node3 = new PropositionNode("the light", "on");
        NextNode nxn2 = new NextNode();
        nxn2.children.add(node3);
        ImpliesNode in = new ImpliesNode();
        in.children.add(an);
        in.children.add(nxn2);
        GlobalNode gn = new GlobalNode();
        gn.children.add(in);

        // Build natural language an print out
        ClauseBuilderVisitor visitor = new ClauseBuilderVisitor(nlgFactory);
        NLGElement clause = visitor.visit(gn);
        System.out.println(realiser.realiseSentence(clause));

    }

}
