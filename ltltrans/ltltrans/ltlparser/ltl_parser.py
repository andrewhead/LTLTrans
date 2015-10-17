#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.InputStream import InputStream
import re

from parser.gen.LtlLexer import LtlLexer as GenLtlLexer
from parser.gen.LtlParser import LtlParser as GenLtlParser
from parser.gen.LtlListener import LtlListener


logging.basicConfig(level=logging.INFO, format="%(message)s")


UNOP_TYPES = {
    'G': 'global',
    'F': 'future',
    'X': 'next',
    '~': 'not',
}

BINOP_TYPES = {
    '->': 'implies',
    'U': 'until',
    '^': 'and',
    'v': 'or',
}


class LtlDictBuilder(LtlListener):

    def to_dict(self, formula):

        self.propositions = []
        self.obj = {}
        self.results = {}

        input = InputStream(formula)
        lexer = GenLtlLexer(input)
        stream = CommonTokenStream(lexer)
        parser = GenLtlParser(stream)
        tree = parser.exp()
        walker = ParseTreeWalker()
        walker.walk(self, tree)

        return {
            'formula': self.obj,
            'propositions': dict(
                [(self.get_prop_index(p), p) for p in self.propositions]
            )
        }

    def exitUnop(self, ctx):
        self.results[ctx] = UNOP_TYPES[ctx.getText()]

    def exitBinop(self, ctx):
        self.results[ctx] = BINOP_TYPES[ctx.getText()]

    def get_prop_index(self, proposition):
        return self.propositions.index(proposition) + 1

    def exitExp(self, ctx):

        obj = None

        # Get nth child of a type for the context
        def _get_child(ctx, type_, index=0):
            matches = filter(
                lambda c: type(c) == type_,
                ctx.children
            )
            return matches[index] if len(matches) > 0 else None

        def _is_terminal(ctx):
            if len(ctx.children) != 1:
                return False
            child = _get_child(ctx, TerminalNodeImpl)
            return type(child) == TerminalNodeImpl

        def _is_proposition(ctx):
            if _is_terminal(ctx):
                return ctx.children[0].symbol.type == GenLtlLexer.PROP

        def _is_unop(ctx):
            return (_get_child(ctx, GenLtlParser.UnopContext) is not None)

        def _is_binop(ctx):
            return (_get_child(ctx, GenLtlParser.BinopContext) is not None)

        def _is_parens(ctx):
            return re.match('^\(.*\)$', ctx.getText())

        if _is_proposition(ctx):
            prop_symbol = ctx.getText()
            self.propositions.append(prop_symbol)
            obj = self.get_prop_index(prop_symbol)

        if _is_unop(ctx):
            op_ctx = _get_child(ctx, GenLtlParser.UnopContext)
            arg = _get_child(ctx, GenLtlParser.ExpContext)
            obj = {
                'unop': {
                    'type': self.results[op_ctx],
                    'arg': self.results[arg]
                }
            }

        if _is_binop(ctx):
            op_ctx = _get_child(ctx, GenLtlParser.BinopContext)
            arg0_ctx = _get_child(ctx, GenLtlParser.ExpContext, 0)
            arg1_ctx = _get_child(ctx, GenLtlParser.ExpContext, 1)
            obj = {
                'binop': {
                    'type': self.results[op_ctx],
                    'arg1': self.results[arg0_ctx],
                    'arg2': self.results[arg1_ctx],
                }
            }

        if _is_parens(ctx):
            child_exp = _get_child(ctx, GenLtlParser.ExpContext)
            obj = self.results[child_exp]

        self.results[ctx] = obj

        if ctx.parentCtx is None:
            self.obj = obj


class LtlParser(object):

    def parse(self, text):
        input = InputStream(text)
        lexer = GenLtlLexer(input)
        stream = CommonTokenStream(lexer)
        parser = GenLtlParser(stream)
        tree = parser.exp()
        return tree.toStringTree()


def main(text):
    parser = LtlParser()
    print parser.parse(text)


if __name__ == '__main__':
    main("XP -> Q")
    main("(XP -> Q) ^ R")
    main("XP -> (Q ^ R)")
