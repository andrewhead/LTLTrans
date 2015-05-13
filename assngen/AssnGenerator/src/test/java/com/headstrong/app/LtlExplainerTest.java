package com.headstrong.app;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import java.util.List;
import java.util.Map;
import java.io.FileReader;
import com.esotericsoftware.yamlbeans.YamlReader;


public class LtlExplainerTest extends TestCase {

    YamlReader formulaReader;
    YamlReader propReader;
    List<Object> formulas;
    List<Object> propositions;
    LtlExplainer explainer;

    public LtlExplainerTest(String testName) throws Exception {
        super(testName);

        // Load some preset propositions and formulas
        formulaReader = new YamlReader(new FileReader("data/formulas.yml"));
        propReader = new YamlReader(new FileReader("data/propositions.yml"));
        formulas = (List<Object>) formulaReader.read();
        propositions = (List<Object>) propReader.read();
        explainer = new LtlExplainer(propositions);
    }

    public static Test suite() {
        return new TestSuite( LtlExplainerTest.class );
    }

    public void testGlobalImplies() throws Exception {
        YamlReader formulaYaml = new YamlReader(
            "unop:\n" +
            "  type: global\n" +
            "  arg:\n" +
            "    binop:\n" +
            "      type: implies\n" +
            "      arg1: 1\n" +
            "      arg2:\n" +
            "        unop:\n" +
            "          type: future\n" +
            "          arg: 2\n"
        );
        YamlReader propYaml = new YamlReader(
            "- subject: a car\n" +
            "  verb: waits in the north-bound direction\n" +
            "- subject: the north-bound green light\n" +
            "  verb: be\n" +
            "  object: on\n"
        );
        Object formula = formulaYaml.read();
        List<Object> props = (List<Object>) propYaml.read();
        LtlExplainer explainer = new LtlExplainer(props);
        assertEquals(
            explainer.render(formula),
            "If a car waits in the north-bound direction then eventually the north-bound green light will be on."
        );
    }

    public void testGlobalNot() throws Exception {
        YamlReader formulaYaml = new YamlReader(
            "unop:\n" +
            "  type: global\n" +
            "  arg:\n" +
            "    unop:\n" +
            "      type: not\n" +
            "      arg:\n" +
            "        binop:\n" +
            "          type: and\n" +
            "          arg1: 1\n" +
            "          arg2: 2\n"
        );
        YamlReader propYaml = new YamlReader(
            "- subject: the north-bound green light\n" +
            "  verb: be\n" +
            "  object: on\n" +
            "- subject: the east-bound green light\n" +
            "  verb: be\n" +
            "  object: on\n"
        );
        Object formula = formulaYaml.read();
        List<Object> props = (List<Object>) propYaml.read();
        LtlExplainer explainer = new LtlExplainer(props);
        assertEquals(
            explainer.render(formula),
            "It is never the case that the north-bound green light is on and the east-bound green light is on."
        );
    }

    public void testImplies() {
        assertEquals(
            explainer.render(formulas.get(0)),
            "If the requester makes a request then the server is available."
        );
    }

    public void testFutureAndUntil() {
        assertEquals(
            explainer.render(formulas.get(1)),
            "At some point it will be the case that the server has low load until the client's stress test begins."
        );
    }

    public void testAnd() {
        assertEquals(
            explainer.render(formulas.get(2)),
            "Currently, the screen is on and the average frame rate is 30fps."
        );
    }

    public void testGlobalFuture() {
        assertEquals(
            explainer.render(formulas.get(3)),
            "Currently, the task is scheduled in the next step or it will be scheduled infinitely often in the future."
        );
    }

    public void testNotFuture() {
        assertEquals(
            explainer.render(formulas.get(4)),
            "At no point in the future will it be that it's always the case that the client makes a request and the request is handled in the next step."
        );
    }

}
