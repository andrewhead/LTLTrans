#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import yaml
import argparse


logging.basicConfig(level=logging.INFO, format="%(message)s")


QUESTION_TEXT =\
"""Problem 1: Understanding Temporal Logic
Interpret the following LTL properties in your own words. Come up with your own real-life propositions to verify for each property. For example, for Gp, you might write, 
"The drone is always 5 feet or more above the ground",
where p is the proposition "5 feet or more above the ground."""


def binop_to_string(binop_type):
    if binop_type == "and":
        return "^"
    elif binop_type == "or":
        return "v"
    elif binop_type == "implies":
        return "⇒"
    elif binop_type == "until":
        return "U"
    else:
        return binop_type


def unop_to_string(unop_type):
    if unop_type == "not":
        return "¬"
    elif unop_type == "next":
        return "X"
    elif unop_type == "future":
        return "F"
    elif unop_type == "global":
        return "G"
    else:
        return unop_type


def propvar_to_string(index):
    return unichr(ord('p') + (index - 1))


def get_argtype(arg):
    if isinstance(arg, dict):
        return arg.keys()[0]
    else:
        return int


def arg_to_string(arg):
    string = ""
    argtype = get_argtype(arg)
    if argtype == int:
        string = propvar_to_string(arg)
    elif argtype == 'binop':
        op = arg['binop']
        string = "{arg1} {op} {arg2}".format(
            arg1=arg_to_string(op['arg1']),
            op=binop_to_string(op['type']),
            arg2=arg_to_string(op['arg2'])
            )
    elif argtype == 'unop':
        op = arg['unop']
        if get_argtype(op['arg']) == 'binop':
            fmt = "{op}({arg})"
        else:
            fmt = "{op}{arg}"
        string = fmt.format(
            arg=arg_to_string(op['arg']),
            op=unop_to_string(op['type']),
            )
    return string


def render(formula):
    return arg_to_string(formula)


def main(filename):
    print QUESTION_TEXT + '\n'
    with open(filename) as formula_file:
        formulas = yaml.load(formula_file.read())
        for i, f in enumerate(formulas, 1):
            print str(i) + '. ' + render(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
        "Generate problem 1 text from formula specifications.")
    parser.add_argument('formula_file', help="YAML file with spec for all formulas")
    args = parser.parse_args()
    main(args.formula_file)

