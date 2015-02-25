# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0002_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('directorio', models.TextField(null=True)),
            ],
            options={
                'db_table': 'grupos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('usuario', models.CharField(max_length=100)),
                ('grupos', models.ManyToManyField(to='dumpserver.Grupo')),
            ],
            options={
                'db_table': 'usuarios',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='base',
            name='grupo_id',
            field=models.ForeignKey(to='dumpserver.Grupo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='servidor_id',
            field=models.ForeignKey(to='dumpserver.Servidor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='base',
            name='contrasenia',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='base',
            name='nombre',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='base',
            name='usuario',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servidor',
            name='ip',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servidor',
            name='motor',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servidor',
            name='nombre',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
