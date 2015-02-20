# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servidor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
                ('ip', models.CharField(max_length=64, null=True)),
                ('puerto', models.IntegerField(null=True)),
                ('motor', models.CharField(max_length=64, null=True)),
                ('descripcion', models.TextField(null=True)),
            ],
            options={
                'db_table': 'servidores',
            },
            bases=(models.Model,),
        ),
    ]
