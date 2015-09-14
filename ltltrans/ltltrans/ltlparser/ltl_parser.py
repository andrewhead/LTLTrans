#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream

from parser.gen.LtlLexer import LtlLexer as GenLtlLexer
from parser.gen.LtlParser import LtlParser as GenLtlParser


logging.basicConfig(level=logging.INFO, format="%(message)s")


class LtlParser(object):

    def parse(text):
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
