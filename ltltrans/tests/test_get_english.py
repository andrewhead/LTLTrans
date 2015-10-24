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
        resp = client.post('/ltl_to_english', {
            'formula': 'p',
            'proposition': 's0',
            'subjects': json.dumps([[
                {'letter': 'p', 'subject': 'the robot', 'verb': 'move', 'object': ''}
            ]]),
        })
        data = json.loads(resp.content)
        self.assertIn("Currently, the robot moves", data['sentence'])

    def test_get_english_for_binary_op(self):
        client = Client()
        resp = client.post('/ltl_to_english', {
            'formula': 'p -> d',
            'proposition': 's0',
            'subjects': json.dumps([[
                {'letter': 'p', 'subject': 'the robot', 'verb': 'move', 'object': ''},
                {'letter': 'd', 'subject': 'the light', 'verb': 'summon', 'object': 'the doctor'},
            ]]),
        })
        data = json.loads(resp.content)
        self.assertIn(
            "Currently, if the robot moves then the light summons the doctor",
            data['sentence']
        )
