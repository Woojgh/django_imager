# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 13:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0002_images'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Images',
        ),
    ]
