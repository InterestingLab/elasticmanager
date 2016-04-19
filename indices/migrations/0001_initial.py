# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'indices_alias',
            },
        ),
        migrations.CreateModel(
            name='Close',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('close_after_days', models.IntegerField()),
            ],
            options={
                'db_table': 'indices_close',
            },
        ),
        migrations.CreateModel(
            name='Create',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_in_advance', models.IntegerField()),
                ('follow_mappings', models.BooleanField()),
            ],
            options={
                'db_table': 'indices_create',
            },
        ),
        migrations.CreateModel(
            name='Delete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delete_after_days', models.IntegerField()),
            ],
            options={
                'db_table': 'indices_delete',
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
                ('created_at', models.DateTimeField()),
                ('status', models.IntegerField(default=0)),
                ('elasticsearch', models.ForeignKey(to='cluster.ElasticCluster')),
            ],
            options={
                'db_table': 'indices_index_set',
            },
        ),
        migrations.CreateModel(
            name='Mappings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mappings', models.TextField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_mappings',
            },
        ),
        migrations.CreateModel(
            name='Optimize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('optimize_after_days', models.IntegerField()),
                ('target_segment_num', models.IntegerField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_optimize',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('settings', models.TextField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_settings',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_snapshot',
            },
        ),
        migrations.AddField(
            model_name='delete',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='create',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='close',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
        migrations.AddField(
            model_name='alias',
            name='index_set',
            field=models.OneToOneField(to='indices.IndexSet'),
        ),
    ]
