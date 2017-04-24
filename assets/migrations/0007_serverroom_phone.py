# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20170420_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverroom',
            name='phone',
            field=models.CharField(default='23', max_length=20, verbose_name='\u673a\u623f\u5730\u5740'),
            preserve_default=False,
        ),
    ]
