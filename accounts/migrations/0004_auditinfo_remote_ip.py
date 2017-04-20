# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170420_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditinfo',
            name='remote_ip',
            field=models.CharField(default=123, max_length=30, verbose_name='\u64cd\u4f5c\u8fdc\u7aefip'),
            preserve_default=False,
        ),
    ]
