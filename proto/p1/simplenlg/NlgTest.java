import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

public class NlgTest {
    
    public static void main(String[] args) {
        benTest();
    }

    public static void benTest() {

        Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        SPhraseSpec c1 = nlgFactory.createClause();
        NPPhraseSpec c1n1 = nlgFactory.createNounPhrase("the light");
        VPPhraseSpec c1v = nlgFactory.createVerbPhrase("be");
        NPPhraseSpec c1n2 = nlgFactory.createNounPhrase("on");
        c1n1.addPreModifier("if");
        c1.setSubject(c1n1);
        c1.setVerb("be");
        c1.setObject(c1n2);
        c1.setFeature(Feature.TENSE, Tense.FUTURE);

        SPhraseSpec c2 = nlgFactory.createClause();
        NPPhraseSpec c2n1 = nlgFactory.createNounPhrase("the door");
        VPPhraseSpec c2v = nlgFactory.createVerbPhrase("be");
        NPPhraseSpec c2n2 = nlgFactory.createNounPhrase("shut");
        c2.setSubject(c2n1);
        c2.setVerb(c2v);
        c2.setObject(c2n2);
        c2.setFeature(Feature.COMPLEMENTISER, "then");
        c1.addComplement(c2);

        String output = realiser.realiseSentence(c1);
        System.out.println(output);

    }

    public static void tutorialTest() {
        Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        SPhraseSpec c = nlgFactory.createClause();
        NPPhraseSpec n1 = nlgFactory.createNounPhrase("Mary");
        VPPhraseSpec v = nlgFactory.createVerbPhrase("chase");
        NPPhraseSpec n2 = nlgFactory.createNounPhrase("the monkey");

        n1.addModifier("quiet");
        v.addModifier("quietly");

        c.setSubject(n1);
        c.setVerb(v);
        c.setObject(n2);
        // c.setFeature(Feature.TENSE, Tense.FUTURE);
        // c.setFeature(Feature.NEGATED, true);

        String output = realiser.realiseSentence(c);
        System.out.println(output);
    }
    
}
