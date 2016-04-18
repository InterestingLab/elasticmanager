# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AliasIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'alias_index_action',
            },
        ),
        migrations.CreateModel(
            name='CloseIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('close_after_days', models.IntegerField()),
            ],
            options={
                'db_table': 'close_index_action',
            },
        ),
        migrations.CreateModel(
            name='CreateIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_in_advance', models.IntegerField()),
                ('follow_mappings', models.BooleanField()),
            ],
            options={
                'db_table': 'create_index_action',
            },
        ),
        migrations.CreateModel(
            name='DeleteIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delete_after_days', models.IntegerField()),
            ],
            options={
                'db_table': 'delete_index_action',
            },
        ),
        migrations.CreateModel(
            name='IndexSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=256, blank=True)),
                ('index_name_prefix', models.CharField(max_length=256)),
                ('index_timestring', models.CharField(max_length=32)),
                ('index_timestring_interval', models.IntegerField(default=1)),
                ('elasticsearch', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField()),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'index_set',
            },
        ),
        migrations.CreateModel(
            name='OptimizeIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('optimize_after_days', models.IntegerField()),
                ('target_segment_num', models.IntegerField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'optimize_index_action',
            },
        ),
        migrations.CreateModel(
            name='SnapshotIndexAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'snapshot_index_action',
            },
        ),
        migrations.AddField(
            model_name='deleteindexaction',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='createindexaction',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='closeindexaction',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='aliasindexaction',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
    ]
