# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-04 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmo_app', '0004_auto_20190303_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventattendee',
            name='attendee_details',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='eventattendee',
            name='attendee_name',
            field=models.CharField(max_length=100),
        ),
    ]