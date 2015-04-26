package com.headstrong.app;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.io.FileReader;
import java.io.IOException;
import com.esotericsoftware.yamlbeans.YamlReader;


public class Problem4 {

    public static void main(String[] args) throws IOException{

        String behaviorsPath = args[0];
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

        // explainer.explainTrace();
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
