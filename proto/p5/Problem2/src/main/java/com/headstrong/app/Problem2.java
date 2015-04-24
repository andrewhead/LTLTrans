package com.headstrong.app;

import java.util.List;
import java.util.Map;
import java.io.FileReader;
import com.esotericsoftware.yamlbeans.YamlReader;


public class Problem2 {

    public static void main( String[] args ) throws Exception {

        // Load propositions and formulas
        YamlReader formulaReader = new YamlReader(new FileReader("data/formulas.yml"));
        YamlReader propReader = new YamlReader(new FileReader("data/propositions.yml"));
        List<Object> formulas = (List<Object>) formulaReader.read();
        List<Object> propositions = (List<Object>) propReader.read();

        System.out.println("Write an LTL property for each of the following specifications. " +
               "Make sure to describe in English what each of your atomic propositions mean.");

        LtlExplainer explainer = new LtlExplainer(propositions);
        for (int fIndex=0; fIndex < formulas.size(); fIndex++) {
            String sentence = explainer.render(formulas.get(fIndex));
            int questionNumber = fIndex + 1;
            System.out.println(questionNumber + ". " + sentence);
        }
    }

}
