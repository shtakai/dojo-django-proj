# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 06:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0005_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
