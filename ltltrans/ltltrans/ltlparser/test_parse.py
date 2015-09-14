#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from ltl_parser import LtlParser


logging.basicConfig(level=logging.INFO, format="%(message)s")


class LtlParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = LtlParser()

    def test_parse_unary_op(self):
        tree = self.parser.parse('Fp')
        self.assertEqual(tree, {
            'unop': {
                'type': 'future',
                'arg': 'p'
            }})


if __name__ == '__main__':
    unittest.main()
