# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import indices.models


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='create',
            name='last_run_at',
            field=models.DateTimeField(default=indices.utils.timenow),
        ),
        migrations.AddField(
            model_name='create',
            name='last_run_info',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='create',
            name='last_run_status',
            field=models.IntegerField(default=0),
        ),
    ]
