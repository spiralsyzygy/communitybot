# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-24 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='groups',
        ),
    ]