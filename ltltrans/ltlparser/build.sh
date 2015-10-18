#! /bin/sh

ANTLR='java -Xmx500M org.antlr.v4.Tool'
SRC_DIR=parser/
OUTPUT_DIR=parser/gen/
CLASSPATH="$CLASSPATH:$OUTPUT_DIR:$SRC_DIR"
GRAMMAR=Ltl.g4

$ANTLR $GRAMMAR -o $OUTPUT_DIR -Dlanguage=Python2
touch $SRC_DIR/__init__.py
touch $OUTPUT_DIR/__init__.py
