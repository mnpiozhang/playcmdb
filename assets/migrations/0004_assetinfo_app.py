# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_remove_applicationinfo_business'),
        ('assets', '0003_assetinfo_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetinfo',
            name='app',
            field=models.ManyToManyField(related_name='asset_application', verbose_name='\u90e8\u7f72\u7684\u5e94\u7528', to='business.ApplicationInfo'),
        ),
    ]
