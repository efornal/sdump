# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_agregar_unique_a_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='directorio',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
