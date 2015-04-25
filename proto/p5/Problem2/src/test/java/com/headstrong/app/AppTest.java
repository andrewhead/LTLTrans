package com.headstrong.app;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import java.util.List;
import java.util.Map;
import java.io.FileReader;
import com.esotericsoftware.yamlbeans.YamlReader;

/**
 * Unit test for simple App.
 */
public class AppTest 
    extends TestCase
{
    YamlReader formulaReader;
    YamlReader propReader;
    List<Object> formulas;
    List<Object> propositions;
    LtlExplainer explainer;

    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public AppTest( String testName ) throws Exception
    {
        super( testName );

        // Load propositions and formulas from predetermined files
        formulaReader = new YamlReader(new FileReader("data/formulas.yml"));
        propReader = new YamlReader(new FileReader("data/propositions.yml"));
        formulas = (List<Object>) formulaReader.read();
        propositions = (List<Object>) propReader.read();
        explainer = new LtlExplainer(propositions);
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( AppTest.class );
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
