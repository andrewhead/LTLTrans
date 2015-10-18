#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from ltltrans.ltlparser.ltl_parser import LtlDictBuilder


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ParseLtlTest(unittest.TestCase):

    def setUp(self):
        self.dict_builder = LtlDictBuilder()

    def test_parse_proposition(self):
        d = self.dict_builder.to_dict('p')
        self.assertEqual(d['formula'], 1)
        self.assertEqual(d['propositions'][1], 'p')

    def test_parse_unop(self):
        d = self.dict_builder.to_dict('Fp')
        self.assertEqual(d['formula'], {
            'unop': {
                'type': 'future',
                'arg': 1
            }
        })
        self.assertEqual(d['propositions'][1], 'p')

    def test_parse_binop(self):
        d = self.dict_builder.to_dict('p ^ q')
        self.assertEqual(d['formula'], {
            'binop': {
                'type': 'and',
                'arg1': 1,
                'arg2': 2,
            }
        })
        self.assertEqual(d['propositions'][1], 'p')
        self.assertEqual(d['propositions'][2], 'q')

    def test_parse_nested_ops(self):
        d = self.dict_builder.to_dict('Fp ^ q')
        self.assertEqual(d['formula'], {
            'binop': {
                'type': 'and',
                'arg1': {
                    'unop': {
                        'type': 'future',
                        'arg': 1,
                    }
                },
                'arg2': 2,
            }
        })
        self.assertEqual(d['propositions'][1], 'p')
        self.assertEqual(d['propositions'][2], 'q')

    def test_parse_preserver_precedence(self):

        # First, try nesting an or operation within an and operation
        d = self.dict_builder.to_dict('p ^ (q v r)')
        self.assertEqual(d['formula'], {
            'binop': {
                'type': 'and',
                'arg1': 1,
                'arg2': {
                    'binop': {
                        'type': 'or',
                        'arg1': 2,
                        'arg2': 3,
                    }
                },
            }
        })

        # Next, reverse the order based on the parentheses placement
        d = self.dict_builder.to_dict('(p ^ q) v r')
        self.assertEqual(d['formula'], {
            'binop': {
                'type': 'or',
                'arg1': {
                    'binop': {
                        'type': 'and',
                        'arg1': 1,
                        'arg2': 2,
                    }
                },
                'arg2': 3,
            }
        })
