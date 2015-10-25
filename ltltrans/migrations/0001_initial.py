# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(max_length=100)),
                ('ltl', models.CharField(max_length=100)),
                ('ipAddr', models.CharField(max_length=32, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('propositions', models.CharField(max_length=300)),
                ('errorType', models.CharField(max_length=64)),
                ('suggestion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='GetEnglishEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(max_length=100)),
                ('ltl', models.CharField(max_length=100)),
                ('ipAddr', models.CharField(max_length=32, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('execTime', models.FloatField()),
                ('propositions', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='GetLtlEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(max_length=100)),
                ('ltl', models.CharField(max_length=100)),
                ('ipAddr', models.CharField(max_length=32, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('execTime', models.FloatField()),
                ('propositions', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='LoadPageEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipAddr', models.CharField(max_length=32, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
