# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\20A\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\4\17\t\17\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3")
        buf.write(u"\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13")
        buf.write(u"\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\17\6\17>\n\17")
        buf.write(u"\r\17\16\17?\2\2\20\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write(u"\n\23\13\25\f\27\r\31\16\33\17\35\20\3\2\4\5\2C\\``c")
        buf.write(u"|\4\2\13\13\"\"A\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2")
        buf.write(u"\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2")
        buf.write(u"\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2")
        buf.write(u"\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\3\37\3\2\2\2\5")
        buf.write(u"!\3\2\2\2\7#\3\2\2\2\t%\3\2\2\2\13\'\3\2\2\2\r)\3\2\2")
        buf.write(u"\2\17+\3\2\2\2\21-\3\2\2\2\23/\3\2\2\2\25\61\3\2\2\2")
        buf.write(u"\27\63\3\2\2\2\31\67\3\2\2\2\33:\3\2\2\2\35=\3\2\2\2")
        buf.write(u"\37 \7*\2\2 \4\3\2\2\2!\"\7+\2\2\"\6\3\2\2\2#$\7I\2\2")
        buf.write(u"$\b\3\2\2\2%&\7H\2\2&\n\3\2\2\2\'(\7Z\2\2(\f\3\2\2\2")
        buf.write(u")*\7\u0080\2\2*\16\3\2\2\2+,\7W\2\2,\20\3\2\2\2-.\7Y")
        buf.write(u"\2\2.\22\3\2\2\2/\60\7`\2\2\60\24\3\2\2\2\61\62\7x\2")
        buf.write(u"\2\62\26\3\2\2\2\63\64\7>\2\2\64\65\7/\2\2\65\66\7@\2")
        buf.write(u"\2\66\30\3\2\2\2\678\7/\2\289\7@\2\29\32\3\2\2\2:;\t")
        buf.write(u"\2\2\2;\34\3\2\2\2<>\t\3\2\2=<\3\2\2\2>?\3\2\2\2?=\3")
        buf.write(u"\2\2\2?@\3\2\2\2@\36\3\2\2\2\4\2?\2")
        return buf.getvalue()


class LtlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    PROP = 13
    WS = 14

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'('", u"')'", u"'G'", u"'F'", u"'X'", u"'~'", u"'U'", u"'W'", 
            u"'^'", u"'v'", u"'<->'", u"'->'" ]

    symbolicNames = [ u"<INVALID>",
            u"PROP", u"WS" ]

    ruleNames = [ u"T__0", u"T__1", u"T__2", u"T__3", u"T__4", u"T__5", 
                  u"T__6", u"T__7", u"T__8", u"T__9", u"T__10", u"T__11", 
                  u"PROP", u"WS" ]

    grammarFileName = u"Ltl.g4"

    def __init__(self, input=None):
        super(LtlLexer, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


