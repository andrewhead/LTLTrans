#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import json
from django.test import Client


logging.basicConfig(level=logging.INFO, format="%(message)s")


class GetEnglishFromLtlTest(unittest.TestCase):

    def test_get_english_for_single_ltl_statement(self):
        client = Client()
        resp = client.get('/ltl_to_english', {
            'ltl': 'P -> Q',
            'propositions': [
                {'subject': "the robot", 'verb': "moves", 'object': ""},
                {'subject': "the light", 'verb': "summons", 'object': "the doctor"},
            ]
        })
        data = json.loads(resp.content)
        self.assertIn("If the robot moves, then the light summons the doctor", data['sentence'])
