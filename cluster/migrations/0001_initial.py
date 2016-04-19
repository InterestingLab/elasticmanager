# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElasticCluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('host', models.CharField(max_length=256)),
                ('port', models.IntegerField()),
            ],
            options={
                'db_table': 'cluster_elastic_cluster',
            },
        ),
    ]
