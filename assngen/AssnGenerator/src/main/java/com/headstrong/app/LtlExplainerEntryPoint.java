package com.headstrong.app;

import java.util.ArrayList;
import py4j.GatewayServer;


public class LtlExplainerEntryPoint {

    public LtlExplainerEntryPoint() {}

    public LtlExplainer getExplainer(ArrayList<Object> propositions) {
        LtlExplainer explainer = new LtlExplainer(propositions);
        return explainer;
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new LtlExplainerEntryPoint(), 25334);
        gatewayServer.start();
        System.out.println("Gateway server started");
    }

}
