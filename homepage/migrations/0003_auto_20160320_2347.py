# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20160320_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='site_copyright',
            field=models.CharField(blank=True, max_length=200, verbose_name='\u7248\u6743\u4fe1\u606f'),
        ),
    ]
