#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from ltltrans.converter import *
import StringIO
import logging
import json
import ast


logging.basicConfig(level=logging.INFO, format="%(message)s")


def hello_world(request):
    return HttpResponse("Hello World!")


def english_to_ltl(request):
    
    sentence = request.GET.get("sentence")
    variables = ast.literal_eval(request.GET.get("variables"))
    
    conv = Converter(sentence, [], False)
    for v in variables.items():
        print "vars",v[0], v[1]
        conv.add_variable(v[0], v[1])
        
    ltl_trans = conv.get_statement()
    if len(ltl_trans) == 0:
        ltl_string = "LTL description could not be translated.  Perhaps it is too complex of a statement."
    else:
        buff = StringIO.StringIO()
        ltl_trans[0].print_statement(buff)
        ltl_string = buff.getvalue()
        buff.close()
        
    return HttpResponse(json.dumps({
        'ltl': ltl_string,
    }))
