#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import Client
import unittest
import logging
import json


logging.basicConfig(level=logging.INFO, format="%(message)s")


class GetLtlTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def testGetLtl(self):
        resp = self.client.post('/english_to_ltl', {
            'sentence': "The robot moves infinitely often",
            'proposition': 's0',
            'subjects': json.dumps([[
                {'letter': 'r', 'subject': 'the robot', 'verb': 'move', 'object': ''},
            ]]),
        })
        data = json.loads(resp.content)
        self.assertEqual(data, {
            'ltl': "G F r"
        })
