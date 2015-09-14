# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .LtlListener import LtlListener
else:
    from LtlListener import LtlListener
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\17*\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\5\2\f\n\2\3")
        buf.write(u"\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2\25\n\2\3\2\3\2\5\2\31")
        buf.write(u"\n\2\3\2\3\2\5\2\35\n\2\3\2\3\2\7\2!\n\2\f\2\16\2$\13")
        buf.write(u"\2\3\3\3\3\3\4\3\4\3\4\2\3\2\5\2\4\6\2\4\3\2\5\7\3\2")
        buf.write(u"\b\r,\2\24\3\2\2\2\4%\3\2\2\2\6\'\3\2\2\2\b\t\b\2\1\2")
        buf.write(u"\t\13\5\4\3\2\n\f\7\17\2\2\13\n\3\2\2\2\13\f\3\2\2\2")
        buf.write(u"\f\r\3\2\2\2\r\16\5\2\2\4\16\25\3\2\2\2\17\20\7\3\2\2")
        buf.write(u"\20\21\5\2\2\2\21\22\7\4\2\2\22\25\3\2\2\2\23\25\7\16")
        buf.write(u"\2\2\24\b\3\2\2\2\24\17\3\2\2\2\24\23\3\2\2\2\25\"\3")
        buf.write(u"\2\2\2\26\30\f\3\2\2\27\31\7\17\2\2\30\27\3\2\2\2\30")
        buf.write(u"\31\3\2\2\2\31\32\3\2\2\2\32\34\5\6\4\2\33\35\7\17\2")
        buf.write(u"\2\34\33\3\2\2\2\34\35\3\2\2\2\35\36\3\2\2\2\36\37\5")
        buf.write(u"\2\2\4\37!\3\2\2\2 \26\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"")
        buf.write(u"#\3\2\2\2#\3\3\2\2\2$\"\3\2\2\2%&\t\2\2\2&\5\3\2\2\2")
        buf.write(u"\'(\t\3\2\2(\7\3\2\2\2\7\13\24\30\34\"")
        return buf.getvalue()


class LtlParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'('", u"')'", u"'G'", u"'F'", u"'X'", 
                     u"'U'", u"'W'", u"'^'", u"'v'", u"'<->'", u"'->'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"PROP", u"WS" ]

    RULE_exp = 0
    RULE_unop = 1
    RULE_binop = 2

    ruleNames =  [ u"exp", u"unop", u"binop" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    PROP=12
    WS=13

    def __init__(self, input):
        super(LtlParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ExpContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(LtlParser.ExpContext, self).__init__(parent, invokingState)
            self.parser = parser

        def unop(self):
            return self.getTypedRuleContext(LtlParser.UnopContext,0)


        def exp(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(LtlParser.ExpContext)
            else:
                return self.getTypedRuleContext(LtlParser.ExpContext,i)


        def WS(self, i=None):
            if i is None:
                return self.getTokens(LtlParser.WS)
            else:
                return self.getToken(LtlParser.WS, i)

        def PROP(self):
            return self.getToken(LtlParser.PROP, 0)

        def binop(self):
            return self.getTypedRuleContext(LtlParser.BinopContext,0)


        def getRuleIndex(self):
            return LtlParser.RULE_exp

        def enterRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.enterExp(self)

        def exitRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.exitExp(self)



    def exp(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LtlParser.ExpContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_exp, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            token = self._input.LA(1)
            if token in [LtlParser.T__2, LtlParser.T__3, LtlParser.T__4]:
                self.state = 7
                self.unop()
                self.state = 9
                _la = self._input.LA(1)
                if _la==LtlParser.WS:
                    self.state = 8
                    self.match(LtlParser.WS)


                self.state = 11
                self.exp(2)

            elif token in [LtlParser.T__0]:
                self.state = 13
                self.match(LtlParser.T__0)
                self.state = 14
                self.exp(0)
                self.state = 15
                self.match(LtlParser.T__1)

            elif token in [LtlParser.PROP]:
                self.state = 17
                self.match(LtlParser.PROP)

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 32
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LtlParser.ExpContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                    self.state = 20
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 22
                    _la = self._input.LA(1)
                    if _la==LtlParser.WS:
                        self.state = 21
                        self.match(LtlParser.WS)


                    self.state = 24
                    self.binop()
                    self.state = 26
                    _la = self._input.LA(1)
                    if _la==LtlParser.WS:
                        self.state = 25
                        self.match(LtlParser.WS)


                    self.state = 28
                    self.exp(2) 
                self.state = 34
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class UnopContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(LtlParser.UnopContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LtlParser.RULE_unop

        def enterRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.enterUnop(self)

        def exitRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.exitUnop(self)




    def unop(self):

        localctx = LtlParser.UnopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_unop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LtlParser.T__2) | (1 << LtlParser.T__3) | (1 << LtlParser.T__4))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BinopContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(LtlParser.BinopContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LtlParser.RULE_binop

        def enterRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.enterBinop(self)

        def exitRule(self, listener):
            if isinstance( listener, LtlListener ):
                listener.exitBinop(self)




    def binop(self):

        localctx = LtlParser.BinopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_binop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LtlParser.T__5) | (1 << LtlParser.T__6) | (1 << LtlParser.T__7) | (1 << LtlParser.T__8) | (1 << LtlParser.T__9) | (1 << LtlParser.T__10))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.exp_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def exp_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         



