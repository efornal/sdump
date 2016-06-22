# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0010_tipo_char_para_atributo_directorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='base',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dumpserver.Grupo'),
        ),
        migrations.AlterField(
            model_name='base',
            name='servidor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dumpserver.Servidor'),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='ip',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='motor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='puerto',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dumpserver.Version'),
        ),
    ]