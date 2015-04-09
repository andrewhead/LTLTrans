#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import random
import argparse


logging.basicConfig(level=logging.INFO, format="%(message)s")


def binary_digits(count):
    return [random.choice(['p', 'a']) for _ in range(count)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('icount', help='count of inputs', type=int)
    parser.add_argument('len', help='length of trace', type=int)
    parser.add_argument('iter', help='number of traces to make', type=int)
    args = parser.parse_args()

    varstr = lambda name,vals : name + '\t' + '\t'.join([str(v) for v in vals])

    for i in range(args.iter):
        for j in range(args.icount):
            print str(i) + '\t' + varstr('x' + str(j), binary_digits(args.len))
        print ""

