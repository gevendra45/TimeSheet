# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-06-03 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20200601_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='logintime',
            name='nwtime',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='logintime',
            name='wtime',
            field=models.FloatField(default=0),
        ),
    ]