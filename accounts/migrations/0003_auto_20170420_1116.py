# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auditinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditinfo',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 20, 11, 16, 15, 76000), verbose_name='\u64cd\u4f5c\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auditinfo',
            name='account',
            field=models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u7528\u6237'),
        ),
    ]
