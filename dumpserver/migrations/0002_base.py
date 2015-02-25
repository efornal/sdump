# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
                ('usuario', models.CharField(max_length=64)),
                ('contrasenia', models.CharField(max_length=64)),
                ('descripcion', models.TextField(null=True)),
            ],
            options={
                'db_table': 'bases',
            },
            bases=(models.Model,),
        ),
    ]
