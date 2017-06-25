# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_images', '0007_auto_20170625_0516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='thumbnails')),
            ],
        ),
    ]
