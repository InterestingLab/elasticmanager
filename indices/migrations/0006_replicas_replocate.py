# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0005_auto_20160522_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replicas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exec_offset', models.IntegerField()),
                ('target_replica_num', models.IntegerField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_replicas',
            },
        ),
        migrations.CreateModel(
            name='Replocate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exec_offset', models.IntegerField()),
                ('target_names', models.TextField()),
                ('target_tags', models.TextField()),
                ('target_racks', models.TextField()),
                ('index_set', models.OneToOneField(to='indices.IndexSet')),
            ],
            options={
                'db_table': 'indices_relocate',
            },
        ),
    ]
