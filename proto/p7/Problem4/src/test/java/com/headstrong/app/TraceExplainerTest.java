package com.headstrong.app;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;


public class TraceExplainerTest extends TestCase {

    public TraceExplainerTest(String testName) {
        super(testName);
    }

    public static Test suite() {
        return new TestSuite(TraceExplainerTest.class);
    }

    public void testSwitchAllCyclesSame() {
        TraceExplainer explainer = new TraceExplainer();
        String exp = explainer.explainTrace(
            "the yellow light",
            SourceType.SWITCH,
            new int[] {1, 1, 1, 1, 1}
        );
        assertEquals(exp, "The yellow light is on for all cycles.");
    }

    public void testSwitchHoldsLastValueMultipleCycles() {
        TraceExplainer explainer = new TraceExplainer();
        String exp = explainer.explainTrace(
            "the red light",
            SourceType.SWITCH,
            new int[] {0, 1, 1, 0, 0}
        );
        assertEquals(exp, "The red light is off for the first cycle, " +
            "turns on for 2 cycles and then turns off for the next 2 cycles " +
            "and remains off.");
    }

    public void testSwitchChangesInLastCycle() {
        TraceExplainer explainer = new TraceExplainer();
        String exp = explainer.explainTrace(
            "the yellow light",
            SourceType.SWITCH,
            new int[] {0, 1, 0, 0, 1}
        );
        assertEquals(exp, "The yellow light is off for the first cycle, " +
            "turns on for 1 cycle, turns off for 2 cycles and then turns on " +
            "for the next cycle and remains on.");
    }

    public void testExplainPureSignal() {
        TraceExplainer explainer = new TraceExplainer();
        String exp = explainer.explainTrace(
            "the up signal",
            SourceType.PURE,
            new int[] {0, 1, 1, 0, 0}
        );
        assertEquals(exp, "The up signal is absent for the first cycle, " +
            "present for 2 cycles and then absent for the next 2 cycles " +
            "and remains absent.");
    }

    public void testExplainIntegerSignal() {
        TraceExplainer explainer = new TraceExplainer();
        String exp = explainer.explainTrace(
            "the counter",
            SourceType.INTEGER,
            new int[] {0, 0, 0, 1, 0}
        );
        assertEquals(exp, "The counter has value 0 for the first 3 cycles, " +
            "rises to value 1 for 1 cycle and then falls to value 0 for the " +
            "next cycle and holds value 0.");
    }

}
