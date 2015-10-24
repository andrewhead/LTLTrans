#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import json
import time
from py4j.java_gateway import JavaGateway, GatewayParameters
from StringIO import StringIO

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from ipware.ip import get_ip

from ltltrans.englishparser.translator import translate
from ltltrans.ltlparser.ltl_parser import LtlDictBuilder
from ltltrans.models import ErrorReport, LoadPageEvent, GetLtlEvent, GetEnglishEvent


logging.basicConfig(level=logging.INFO, format="%(message)s")
request_logger = logging.getLogger('request')


PROPOSITION_GROUPS = [
    {
        'propositions': [
            {
                'subject': 'the robot',
                'verb': 'move',
                'letter': 'r',
                'sentence': "the robot moves"
            },
            {
                'subject': 'the light',
                'verb': 'flashe',
                'letter': 'l',
                'sentence': "the light flashes"
            },
        ],
        'example': {
            'formula': 'G(r -> Fl)',
            'sentence': "If the robot moves then eventually the light will flash.",
        }
    },
    {
        'propositions': [
            {
                'subject': 'the brake',
                'verb': 'engage',
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
                'subject': 'the light',
                'verb': 'dim',
                'letter': 'l',
                'sentence': "the light dims",
            },
            {
                'subject': 'the sensor',
                'verb': 'trigger',
                'letter': 's',
                'sentence': "the sensor triggers",
            },
            {
                'subject': 'the alarm',
                'verb': 'sound',
                'letter': 'a',
                'sentence': "the alarm sounds",
            },
        ],
        'example': {
            'formula': 'G((l ^ s) -> Xa)',
            'sentence': "If the light dims and the sensor triggers then the alarm sounds " +
                        "in the next step."
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
    context = {
        'propositions': PROPOSITION_GROUPS,
        'text': 'If the robot will eventually move, then the light always blinks.',
        'ltl': 'Fp -> Gq',
    }
    LoadPageEvent.objects.create(
        ipAddr=get_ip(request),
    )
    return render(request, 'ltltrans/home.html', context)


def get_propositions(propname, defaults, custom):
    if propname.startswith('s'):
        prop_index = int(propname.replace('s', ''))
        props = custom[prop_index]
    else:
        prop_index = int(propname)
        props = defaults[prop_index]['propositions']
    return props


def english_to_ltl(request):

    start_time = time.time()
    sentence = request.POST.get("sentence")
    prop = request.POST.get('proposition')
    custom_subjects = json.loads(request.POST.get('subjects'))
    props = get_propositions(prop, PROPOSITION_GROUPS, custom_subjects)

    statement = translate(sentence, props)
    buff = StringIO()
    statement.print_statement(buff, True)
    ltl = buff.getvalue()

    if len(ltl) == 0:
        ltl = "LTL description could not be translated. " +\
            "Perhaps it is too complex of a statement."

    GetLtlEvent.objects.create(
        sentence=sentence,
        ltl=ltl,
        propositions=json.dumps(props),
        ipAddr=get_ip(request),
        execTime=time.time() - start_time,
    )

    return HttpResponse(json.dumps({
        'ltl': ltl,
    }), content_type="application/json")


def ltl_to_english(request):

    start_time = time.time()
    ltl = request.POST.get('formula')
    prop = request.POST.get('proposition')
    custom_subjects = json.loads(request.POST.get('subjects'))
    props = get_propositions(prop, PROPOSITION_GROUPS, custom_subjects)

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

    GetEnglishEvent.objects.create(
        sentence=explanation,
        ltl=ltl,
        propositions=json.dumps(props),
        ipAddr=get_ip(request),
        execTime=time.time() - start_time,
    )

    return HttpResponse(json.dumps({
        'sentence': explanation,
    }), content_type="application/json")


def report_error(request):
    prop = request.POST.get('proposition')
    custom_subjects = json.loads(request.POST.get('subjects'))
    props = get_propositions(prop, PROPOSITION_GROUPS, custom_subjects)
    ErrorReport.objects.create(
        sentence=request.POST.get('sentence'),
        ltl=request.POST.get('formula'),
        propositions=json.dumps(props),
        ipAddr=get_ip(request),
    )
    return HttpResponse()
