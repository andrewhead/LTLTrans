package com.headstrong.app;

import java.util.List;
import java.util.Map;
import java.io.FileReader;
import com.esotericsoftware.yamlbeans.YamlReader;


public class Problem3 {

    public static void main( String[] args ) throws Exception {

        String purpose = args[0];
        String propositionsPath = args[1];
        String formulasPath = args[2];

        // Load propositions and formulas
        YamlReader formulaReader = new YamlReader(new FileReader(formulasPath));
        YamlReader propReader = new YamlReader(new FileReader(propositionsPath));
        List<Object> formulas = (List<Object>) formulaReader.read();
        List<Object> propositions = (List<Object>) propReader.read();

        System.out.println();
        System.out.println("Problem 3.  Designing Models from Specifications.");
        System.out.println("Design an automata for " + purpose + " that satisfies the following:");
        System.out.println();

        LtlExplainer explainer = new LtlExplainer(propositions);
        for (Object formula: formulas) {
            String sentence = explainer.render(formula);
            System.out.print(sentence + " ");
        }
        System.out.println();
        System.out.println();

    }

}
