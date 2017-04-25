# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auditinfo_remote_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditinfo',
            name='type',
            field=models.CharField(default='abc', max_length=30, verbose_name='\u64cd\u4f5c\u7c7b\u578b'),
            preserve_default=False,
        ),
    ]
