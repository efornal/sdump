# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-02-10 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_change_sort_meta_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servidor',
            name='puerto',
            field=models.IntegerField(default=5432, verbose_name='puerto'),
            preserve_default=False,
        ),
    ]
