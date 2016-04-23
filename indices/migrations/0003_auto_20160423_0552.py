# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import indices.utils


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0002_auto_20160422_0329'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskExec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0)),
                ('last_run_at', models.DateTimeField(default=indices.utils.timenow)),
                ('last_run_status', models.IntegerField(default=0)),
                ('last_run_info', models.TextField(default='')),
            ],
            options={
                'db_table': 'indices_tasks',
            },
        ),
        migrations.RemoveField(
            model_name='create',
            name='last_run_at',
        ),
        migrations.RemoveField(
            model_name='create',
            name='last_run_info',
        ),
        migrations.RemoveField(
            model_name='create',
            name='last_run_status',
        ),
        migrations.AlterField(
            model_name='indexset',
            name='created_at',
            field=models.DateTimeField(default=indices.utils.timenow),
        ),
        migrations.AddField(
            model_name='taskexec',
            name='index_set',
            field=models.ForeignKey(to='indices.IndexSet'),
        ),
    ]
