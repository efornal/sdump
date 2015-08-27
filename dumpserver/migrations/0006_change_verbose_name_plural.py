# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0005_auto_20150225_1558'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='base',
            options={'verbose_name_plural': 'Bases'},
        ),
        migrations.AlterModelOptions(
            name='grupo',
            options={'verbose_name_plural': 'Grupos'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name_plural': 'Usuarios'},
        ),
    ]
