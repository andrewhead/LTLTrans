#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import StringIO
import json
import ast
from time import strftime
import time
from py4j.java_gateway import JavaGateway, GatewayParameters

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from ltltrans.converter import Converter
from ltltrans.ltlparser.ltl_parser import LtlDictBuilder


logging.basicConfig(level=logging.INFO, format="%(message)s")
request_logger = logging.getLogger('request')


PROPOSITION_GROUPS = [
    {
        'propositions': [
            {
                'subject': 'the robot',
                'verb': 'moves',
                'letter': 'r',
                'sentence': "the robot moves"
            },
            {
                'subject': 'the light',
                'verb': 'turn',
                'object': 'on',
                'letter': 'l',
                'sentence': "the light turns on"
            },
        ],
        'example': {
            'formula': 'G(r -> Fl)',
            'sentence': "If the robot moves then eventually the light will turn on.",
        }
    },
    {
        'propositions': [
            {
                'subject': 'the brake',
                'verb': 'engages',
                'letter': 'b',
                'sentence': "the brake engages",
            }
        ],
        'example': {
            'formula': 'Fb',
            'sentence': "At some point it will be the case that the brake engages.",
        }
    },
    {
        'propositions': [
            {
                'subject': 'thread 1',
                'verb': 'finishes',
                'letter': 't',
                'sentence': "thread 1 finishes",
            },
            {
                'subject': 'thread 2',
                'verb': 'finishes',
                'letter': 'u',
                'sentence': "thread 2 finishes",
            },
            {
                'subject': 'the process',
                'verb': 'exit',
                'letter': 'p',
                'sentence': "the process exists",
            },
        ],
        'example': {
            'formula': 'G((t ^ u) -> Xp)',
            'sentence': "If thread 1 finishes and thread 2 finishes then the process exits" +
                        "in the next step.",
        }
    },
]

''' Our LTL explainer is implemented in Java, so we open up a gateway through Py4J for now. '''
gateway = JavaGateway(
    gateway_parameters=GatewayParameters(
        port=settings.PY4J_PORT,
        auto_convert=True,  # automatically convert Python data structures to  Java ones
    ))


def hello_world(request):
    return HttpResponse("Hello World!")


def home(request):
    start_timestamp = strftime("%Y-%m-%d %H:%M:%S")
    context = {
        'propositions': PROPOSITION_GROUPS,
        'text': 'If the robot will eventually move, then the light always blinks.',
        'ltl': 'Fp -> Gq',
    }
    request_logger.info(
        "Visited 'home'. IP: %s,,, Start Time: %s,,, ",
        request.META['REMOTE_ADDR'],
        start_timestamp,
        )
    return render(request, 'ltltrans/home.html', context)


def english_to_ltl(request):

    start_timestamp = strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()
    sentence = request.GET.get("sentence")
    variables = ast.literal_eval(request.GET.get("variables"))

    conv = Converter(sentence, [], False)
    for v in variables.items():
        # print "vars", v[0], v[1]
        conv.add_variable(v[0], v[1])

    ltl_trans = conv.get_statement()
    if len(ltl_trans) == 0:
        ltl_string = "LTL description could not be translated. " +\
            "Perhaps it is too complex of a statement."
    else:
        buff = StringIO.StringIO()
        ltl_trans[0].print_statement(buff)
        ltl_string = buff.getvalue()
        buff.close()

    request_logger.info(
        "Visited 'english_to_ltl'. IP: %s,,, Start Time: %s,,, Execution Time: %f,,, " +
        "Sentence: %s,,, Variables: %s,,, Result: %s,,,",
        request.META['REMOTE_ADDR'],
        start_timestamp,
        time.time() - start_time,
        sentence,
        json.dumps(variables),
        ltl_string,
        )

    return HttpResponse(json.dumps({
        'ltl': ltl_string,
    }))


def ltl_to_english(request):

    start_timestamp = strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()
    ltl = request.POST.get('formula')
    prop = request.POST.get('proposition')
    custom_subjects = json.loads(request.POST.get('subjects'))

    if prop.startswith('s'):
        prop_index = int(prop.replace('s', ''))
        props = custom_subjects[prop_index]
    else:
        prop_index = int(prop)
        props = PROPOSITION_GROUPS[prop_index]['propositions']

    dict_builder = LtlDictBuilder()
    res = dict_builder.to_dict(ltl)
    formula_dict = res['formula']
    propnames_parsed = res['propositions']

    propnames_ordered = [t[1] for t in sorted(propnames_parsed.items(), key=lambda t: t[0])]
    props_ordered = []
    for pn in propnames_ordered:
        props_ordered.append(filter(lambda p: p['letter'] == pn, props)[0])

    explainer = gateway.entry_point.getExplainer(props_ordered)
    explanation = explainer.render(formula_dict)

    request_logger.info(
        "Visited 'ltl_to_english'. IP: %s,,, Start Time: %s,,, Execution Time: %f,,, " +
        "Formula: %s,,, Propositions: %s,,, Result: %s,,,",
        request.META['REMOTE_ADDR'],
        start_timestamp,
        time.time() - start_time,
        ltl,
        json.dumps(props),
        explanation,
        )

    return HttpResponse(json.dumps({
        'sentence': explanation,
    }), content_type="application/json")
