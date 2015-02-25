# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0004_auto_20150223_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servidor',
            options={'verbose_name_plural': 'Servidores'},
        ),
    ]
