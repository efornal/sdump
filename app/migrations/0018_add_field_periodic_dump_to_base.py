# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-13 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_add_field_password_id_to_base'),
    ]

    operations = [
        migrations.AddField(
            model_name='base',
            name='periodic_dump',
            field=models.BooleanField(default=False, verbose_name='periodic_dump'),
        ),
        migrations.AlterField(
            model_name='base',
            name='password_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Id contrase\xf1a (rattic)'),
        ),
    ]
