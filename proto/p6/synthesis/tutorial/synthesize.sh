#! /bin/bash
# Requires Lily from http://www.iaik.tugraz.at/content/research/opensource/lily/
lily.pl -syn trafficlight.part -ltl trafficlight.ltl -syndir output
dot -Tps output/ltl2vl-synthesis.dot -o model_viz.ps
