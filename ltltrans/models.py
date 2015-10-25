#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from django.db import models


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ErrorReport(models.Model):
    sentence = models.CharField(max_length=100)
    ltl = models.CharField(max_length=100)
    ipAddr = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    propositions = models.CharField(max_length=300)
    errorType = models.CharField(max_length=64)
    suggestion = models.CharField(max_length=300)


class LoadPageEvent(models.Model):
    ipAddr = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class GetLtlEvent(models.Model):
    sentence = models.CharField(max_length=100)
    ltl = models.CharField(max_length=100)
    ipAddr = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    execTime = models.FloatField()
    propositions = models.CharField(max_length=300)


class GetEnglishEvent(models.Model):
    sentence = models.CharField(max_length=100)
    ltl = models.CharField(max_length=100)
    ipAddr = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    execTime = models.FloatField()
    propositions = models.CharField(max_length=300)
