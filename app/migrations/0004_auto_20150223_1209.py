# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150223_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='base',
            old_name='grupo_id',
            new_name='grupo',
        ),
        migrations.RenameField(
            model_name='base',
            old_name='servidor_id',
            new_name='servidor',
        ),
    ]
