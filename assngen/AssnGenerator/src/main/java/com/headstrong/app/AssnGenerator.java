package com.headstrong.app;

import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import com.esotericsoftware.yamlbeans.YamlReader;


public class AssnGenerator {

    public static void main( String[] args ) throws Exception {
        problem1(
            "data/formulas_p1.yml"
        );
        problem2(
            "data/formulas_p2.yml",
            "data/propositions_p2.yml"
        );
        problem3(
            "traffic light control",
            "data/formulas_p3.yml",
            "data/propositions_p3.yml"
        );
        problem4(
            "data/behaviors_p4.yml"
        );
        problem2(
            "data/formulas_paper_ltl1.yml",
            "data/propositions_paper_ltl1.yml"
        );
        problem4(
            "data/behaviors_paper.yml"
        );
    }

    public static void problem1(String formulasPath) throws IOException {
        System.out.println();
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"python", "python/problem1.py", formulasPath};
        Process proc = rt.exec(commands);
        BufferedReader stdOutput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
        String s = null;
        while ((s = stdOutput.readLine()) != null) {
            System.out.println(s);
        }
        while ((s = stdError.readLine()) != null) {
            System.out.println(s);
        }
        System.out.println();
    }

    public static void problem2(String formulasPath, String propositionsPath) throws Exception {
        // Load propositions and formulas
        YamlReader formulaReader = new YamlReader(new FileReader(formulasPath));
        YamlReader propReader = new YamlReader(new FileReader(propositionsPath));
        List<Object> formulas = (List<Object>) formulaReader.read();
        List<Object> propositions = (List<Object>) propReader.read();

        System.out.println("\n");
        System.out.println("Problem 2.  Converting Specifications to Temporal Logic.");
        System.out.println("Write an LTL property for each of the following specifications. " +
               "Make sure to describe in English what each of your atomic propositions mean.");

        LtlExplainer explainer = new LtlExplainer(propositions);
        for (int fIndex=0; fIndex < formulas.size(); fIndex++) {
            String sentence = explainer.render(formulas.get(fIndex));
            int questionNumber = fIndex + 1;
            System.out.println(questionNumber + ". " + sentence);
        }
        System.out.println("\n");
    }

    public static void problem3(String purpose, String formulasPath, String propositionsPath) throws Exception {

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

    public static void problem4(String behaviorsPath) throws Exception {
        YamlReader behaviorsReader = new YamlReader(new FileReader(behaviorsPath));
        Map behaviorSpec = (Map) behaviorsReader.read();

        List<Object> inputs = (List<Object>) behaviorSpec.get("inputs");
        List<Object> outputs = (List<Object>) behaviorSpec.get("outputs");
        List<List<List<String>>> behaviors = (List<List<List<String>>>) behaviorSpec.get("behaviors");

        List<Map> actors = new ArrayList<Map>();
        for (Object i: inputs) actors.add((Map) i);
        for (Object o: outputs) actors.add((Map) o);

        char subproblem = 'a';
        System.out.println();
        System.out.println("Problem 4.  Understanding model behaviors.");
        System.out.println("Take the following state machine: ");
        System.out.println();
        System.out.println("Inputs:");
        for (Object i: inputs) printActor((Map) i);
        System.out.println("Outputs:");
        for (Object o: outputs) printActor((Map) o);
        System.out.println();
        System.out.println("Which of the following are valid behaviors for the machine?");

        TraceExplainer explainer = new TraceExplainer();
        for (List<List<String>> behavior: behaviors) {
            System.out.print("(" + subproblem + ") ");
            for (int i = 0; i < behavior.size(); i++) {
                List<String> actorBehavior = behavior.get(i);
                Map actor = actors.get(i);
                int[] sequence = new int[actorBehavior.size()];
                for (int j = 0; j < actorBehavior.size(); j++) {
                    sequence[j] = Integer.parseInt(actorBehavior.get(j));
                }
                String exp = explainer.explainTrace(
                    (String) actor.get("name"),
                    getType((String) actor.get("type")),
                    sequence
                );
                System.out.print(exp + " ");
            }
            System.out.println();
            subproblem++;
        }
        System.out.println();
    }

    private static void printActor(Map actor) {
        SourceType type = getType((String) actor.get("type"));
        List<String> values = getValues(type);
        String valuesString = "";
        for (int i = 0; i < values.size(); i++) {
            valuesString += values.get(i);
            if (i < values.size() - 1) valuesString += ", ";
        }
        System.out.printf("%s: {%s}\n",
            (String) actor.get("name"),
            valuesString
        );
    }

    private static List<String> getValues(SourceType sType) {
        if (sType == SourceType.SWITCH) return Arrays.asList("on", "off");
        else if (sType == SourceType.PURE) return Arrays.asList("absent", "present");
        else if (sType == SourceType.INTEGER) return Arrays.asList("<integer>");
        else return Arrays.asList("unknown");
    }

    private static SourceType getType(String typeName) {
        if (typeName.equals("switch")) return SourceType.SWITCH;
        else if (typeName.equals("pure")) return SourceType.PURE;
        else if (typeName.equals("integer")) return SourceType.INTEGER;
        else return null;
    }

}
