# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-06-01 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_auto_20200601_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logintime',
            name='rdate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]