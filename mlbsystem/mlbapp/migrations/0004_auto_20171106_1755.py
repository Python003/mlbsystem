# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 09:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlbapp', '0003_auto_20171106_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='backboard',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='backboard',
            name='backtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 6, 17, 55, 59, 843273)),
        ),
    ]
