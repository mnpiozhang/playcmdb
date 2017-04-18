# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetinfo',
            name='mac',
            field=models.CharField(default='sdfsdf', max_length=20, verbose_name='MAC\u5730\u5740'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assetinfo',
            name='asset_name',
            field=models.CharField(unique=True, max_length=40, verbose_name='\u8bbe\u5907\u540d\u79f0'),
        ),
    ]
