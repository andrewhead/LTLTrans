#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import json
from django.test import Client


logging.basicConfig(level=logging.INFO, format="%(message)s")


class GetEnglishFromLtlTest(unittest.TestCase):

    def test_get_english_for_proposition(self):
        client = Client()
        resp = client.get('/ltl_to_english', {
            'ltl': 'P',
            'propositions': json.dumps([
                {'subject': "the robot", 'verb': "moves", 'object': ""},
            ]),
        })
        data = json.loads(resp.content)
        self.assertIn("Currently, the robot moves", data['sentence'])

    def test_get_english_for_binary_op(self):
        client = Client()
        resp = client.get('/ltl_to_english', {
            'ltl': 'P -> Q',
            'propositions': json.dumps([
                {'subject': "the robot", 'verb': "moves", 'object': ""},
                {'subject': "the light", 'verb': "summons", 'object': "the doctor"},
            ]),
        })
        data = json.loads(resp.content)
        self.assertIn(
            "Currently, if the robot moves then the light summons the doctor",
            data['sentence']
        )
