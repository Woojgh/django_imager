# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 09:50
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_images', '0008_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to='thumbnails'),
        ),
    ]