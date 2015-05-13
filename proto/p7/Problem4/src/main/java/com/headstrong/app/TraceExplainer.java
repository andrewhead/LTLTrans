package com.headstrong.app;

import java.util.ArrayList;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;


public class TraceExplainer {

    private Lexicon mLexicon;
    private NLGFactory mNlgFactory;
    private Realiser mRealiser;

    private class ValueCount {
        public int value;
        public int count;
    }

    public TraceExplainer() {
        this.mLexicon = Lexicon.getDefaultLexicon();
        this.mNlgFactory = new NLGFactory(this.mLexicon);
        this.mRealiser = new Realiser(this.mLexicon);
    }

    private ArrayList<ValueCount> aggregateCounts(int[] values) {
        ArrayList<ValueCount> valueCounts = new ArrayList<ValueCount>();
        int count = 0;
        int lastValue = 0;
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                // Add count for previous number if we just switched
                if (values[i] != lastValue) {
                    ValueCount newCount = new ValueCount();
                    newCount.value = lastValue;
                    newCount.count = count;
                    valueCounts.add(newCount);
                    count = 0;
                } 
                // Add count for the very last number in the list
                if (i == values.length - 1) {
                    ValueCount newCount = new ValueCount();
                    newCount.value = values[i];
                    newCount.count = count + 1;
                    valueCounts.add(newCount);
                }
            }
            count ++;
            lastValue = values[i];
        }
        return valueCounts;
    }

    private VPPhraseSpec makeVerb(SourceType sType, boolean transition, int oldValue, int newValue) {
        VPPhraseSpec verb = mNlgFactory.createVerbPhrase("");
        if (sType == SourceType.SWITCH) {
            if (transition == true) {
                verb.setVerb("turn");
            } else {
                verb.setVerb("be");
            }
        } else if (sType == SourceType.PURE) {
            if (transition == false) {
                verb.setVerb("be");
            } else {
                return null;
            }
        } else if (sType == SourceType.INTEGER) {
            if (transition == false) {
                verb.setVerb("have");
            } else {
                PPPhraseSpec prep = mNlgFactory.createPrepositionPhrase();
                prep.setPreposition("to");
                if (newValue > oldValue) {
                    verb.setVerb("rise");
                } else {
                    verb.setVerb("fall");
                }
                verb.addComplement(prep);
            }
        }
        return verb;
    }

    private VPPhraseSpec makeHoldsVerb(SourceType sType) {
        VPPhraseSpec verb = mNlgFactory.createVerbPhrase("");
        if (sType == SourceType.SWITCH) {
            verb.setVerb("remain");
        } else if (sType == SourceType.PURE) {
            verb.setVerb("remain");
        } else if (sType == SourceType.INTEGER) {
            verb.setVerb("hold");
        }
        return verb;
    }

    private NPPhraseSpec makeObject(SourceType sType, int value) {
        NPPhraseSpec obj = mNlgFactory.createNounPhrase("");
        if (sType == SourceType.SWITCH) {
            if (value == 0) {
                obj.setNoun("off");
            } else {
                obj.setNoun("on");
            }
        } else if (sType == SourceType.PURE) {
            if (value == 0) {
                obj.setNoun("absent");
            } else {
                obj.setNoun("present");
            }
        } else if (sType == SourceType.INTEGER) {
            obj.setNoun(Integer.toString(value));
            obj.addPreModifier("value");
        }
        return obj;
    }

    private SPhraseSpec addCycleCount(SPhraseSpec clause, int count) {
        return addCycleCount(clause, count, null);
    }

    private SPhraseSpec addCycleCount(SPhraseSpec clause, int count, String qualifier) {
        return addCycleCount(clause, count, qualifier, false);
    }

    private SPhraseSpec addCycleCount(SPhraseSpec clause, int count, String qualifier, boolean global) {

        PPPhraseSpec prep = mNlgFactory.createPrepositionPhrase();
        prep.setPreposition("for");

        NPPhraseSpec cycles = mNlgFactory.createNounPhrase("cycle");
        String counter = "";
        if (qualifier != null) {
            cycles.setDeterminer("the");
            counter = qualifier + " ";
        }
        if (count > 1) {
            cycles.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
        } else {
            cycles.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR);
        }
        if (global == false && (qualifier == null || count != 1)) {
            counter += Integer.toString(count);
        } else if (global == true) {
            counter = "all " + counter;
        }
        cycles.addPreModifier(counter);

        prep.addComplement(cycles);
        clause.addComplement(prep);
        return clause;

    }

    private SPhraseSpec makeFirstClause(String subj, SourceType sType, ValueCount vc) {
        SPhraseSpec clause = mNlgFactory.createClause();
        clause.setSubject(subj);
        clause.setVerb(makeVerb(sType, false, vc.value, vc.value));
        clause.setObject(makeObject(sType, vc.value));
        clause = addCycleCount(clause, vc.count, "first");
        return clause;
    }

    private SPhraseSpec makeMiddleClause(SourceType sType, ValueCount vc, ValueCount lastVc) {
        SPhraseSpec clause = mNlgFactory.createClause();
        clause.setVerb(makeVerb(sType, true, lastVc.value, vc.value));
        clause.setObject(makeObject(sType, vc.value));
        clause = addCycleCount(clause, vc.count);
        return clause;
    }

    private SPhraseSpec makeLastClause(SourceType sType, ValueCount vc, ValueCount lastVc) {
        SPhraseSpec clause = mNlgFactory.createClause();
        clause.setVerb(makeVerb(sType, true, lastVc.value, vc.value));
        clause.setObject(makeObject(sType, vc.value));
        clause = addCycleCount(clause, vc.count, "next");
        SPhraseSpec holdsClause = mNlgFactory.createClause();
        holdsClause.setVerb(makeHoldsVerb(sType));
        holdsClause.setObject(makeObject(sType, vc.value));
        holdsClause.setFeature(Feature.COMPLEMENTISER, "and");
        clause.addComplement(holdsClause);
        return clause;
    }

    private SPhraseSpec makeTotalClause(String subj, SourceType sType, ValueCount vc) {
        SPhraseSpec clause = mNlgFactory.createClause();
        clause.setSubject(subj);
        clause.setVerb(makeVerb(sType, false, vc.count, vc.count));
        clause.setObject(makeObject(sType, vc.value));
        clause = addCycleCount(clause, vc.count, null, true);
        return clause;
    }

    public String explainTrace(String subj, SourceType sType, int[] values) {
        
        // Aggregate counts for each value in the trace
        ArrayList<ValueCount> valueCounts = aggregateCounts(values);

        // Generate clauses for each value count
        ArrayList<SPhraseSpec> clauses = new ArrayList<SPhraseSpec>();
        if (valueCounts.size() > 1) {
            clauses.add(makeFirstClause(subj, sType, valueCounts.get(0)));
            for (int i = 1 ; i < valueCounts.size() - 1; i++) {
                clauses.add(makeMiddleClause(sType, valueCounts.get(i), valueCounts.get(i - 1)));
            }
            int lastIndex = valueCounts.size() - 1;
            clauses.add(makeLastClause(sType, valueCounts.get(lastIndex), valueCounts.get(lastIndex - 1)));
        } else {
            clauses.add(makeTotalClause(subj, sType, valueCounts.get(0)));
        }

        // Create and realise coordinated phrase
        CoordinatedPhraseElement sentence = mNlgFactory.createCoordinatedPhrase();
        sentence.setConjunction("and then");
        for (int i = 0; i < clauses.size(); i++) {
            sentence.addCoordinate(clauses.get(i));
        }
        return mRealiser.realiseSentence(sentence);
    }

}
