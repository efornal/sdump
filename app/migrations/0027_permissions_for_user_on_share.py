# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-23 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_change_meta_on_share'),
    ]

    operations = [
        migrations.RunSQL(
            [("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sdump_user;")],
            [],
        ),
        migrations.RunSQL(
            [("GRANT SELECT,INSERT,DELETE,UPDATE ON ALL TABLES IN SCHEMA public TO sdump_user;")],
            [("REVOKE ALL PRIVILEGES ON SCHEMA public FROM sdump_user;")],
        ),
    ]