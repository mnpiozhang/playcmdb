# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
        ('assets', '0002_auto_20170418_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetinfo',
            name='business',
            field=models.ManyToManyField(related_name='asset_business', verbose_name='\u5f52\u5c5e\u7684\u4e1a\u52a1\u6761\u7ebf', to='business.BusinessInfo'),
        ),
    ]
