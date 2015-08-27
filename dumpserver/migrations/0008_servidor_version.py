# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dumpserver', '0007_add_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='version',
            field=models.ForeignKey(to='dumpserver.Version', null=True),
        ),
    ]
