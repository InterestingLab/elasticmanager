# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0004_auto_20160423_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mappings',
            name='index_set',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='index_set',
        ),
        migrations.AddField(
            model_name='create',
            name='follow_settings',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='create',
            name='mappings',
            field=models.OneToOneField(null=True, default=None, to='indices.Mappings'),
        ),
        migrations.AddField(
            model_name='create',
            name='settings',
            field=models.OneToOneField(null=True, default=None, to='indices.Settings'),
        ),
        migrations.AlterField(
            model_name='create',
            name='follow_mappings',
            field=models.BooleanField(default=True),
        ),
    ]
