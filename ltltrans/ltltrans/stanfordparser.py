#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import argparse
import subprocess
import os.path
import re
from tempfile import NamedTemporaryFile


logging.basicConfig(level=logging.INFO, format="%(message)s")
SP_PATH = "/usr/local/Cellar/stanford-parser/3.4/libexec"


class TypedDependency(object):
    """ Data structure for Stanford Parser typed dependencies. """

    def __init__(self, name, governor, dependent):
        self.name = name
        self.governor = governor
        self.dependent = dependent


def parse_sentence(text):
    """ Parse sentence with Stanford Parser and return typed dependencies. """

    ''' Write text to temporary file. '''
    tempFile = NamedTemporaryFile(mode='w', delete=False)
    tempFile.write(text)
    tempFile.close()

    ''' Get typed dependencies from running SP. '''
    output = ""
    try:
        output = subprocess.check_output(
            "java " +
            "-cp " + SP_PATH + "/stanford-parser.jar " +
            "-mx200m " +
            "edu.stanford.nlp.parser.lexparser.LexicalizedParser " +
            "-retainTmpSubCategories " +
            "-outputFormat \"typedDependencies\" " +
            "-outputFormatOptions \"basicDependencies\" " +
            "englishPCFG.ser.gz " +
            os.path.abspath(tempFile.name),
        shell=True,
        stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as c:
        print "========ERROR running Stanford Parser========"
        print c.output
    os.remove(tempFile.name)

    ''' Process dependencies. '''
    deps = []
    for line in output.split("\n"):
        match = re.match("([a-z]+)\(([a-zA-Z]+-[0-9]+), ([a-zA-Z]+-[0-9]+)\)", line.strip()) #dependencies should include the numbers after the words
        #match = re.match("([a-z]+)\((.*)?-\d+, (.*)?-\d+\)", line.strip())
        if bool(match):
            dep = TypedDependency(match.group(1), match.group(2), match.group(3))
            deps.append(dep)

    return deps


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help="Text to process")
    args = parser.parse_args()

    deps = parse_sentence(args.text)
    print "=====Dependencies====="
    for dep in deps:
        print "{type}: {gov}, {dep}".format(type=dep.name, gov=dep.governor, dep=dep.dependent)

