#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import Client
import unittest
import logging
import json


logging.basicConfig(level=logging.INFO, format="%(message)s")


class GetLtlTest(unittest.TestCase):

    def testGetLtl(self):
        pass
        """
        client = Client()
        resp = client.get('/english_to_ltl', {
            'sentence': 'The robot moves infinitely often',
            'variables': {
                'm': 'The robot moves.',
            },
        })
        print resp.__dict__
        data = json.loads(resp.content)
        self.assertEqual(data, {'ltl': 'GFm'})
        """
