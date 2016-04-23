# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0003_auto_20160423_0552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskexec',
            old_name='index_set',
            new_name='indexset',
        ),
    ]
