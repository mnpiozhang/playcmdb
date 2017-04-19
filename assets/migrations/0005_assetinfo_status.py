# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_assetinfo_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetinfo',
            name='status',
            field=models.CharField(default=b'd', max_length=1, choices=[(b'd', b'\xe4\xb8\x8b\xe6\x9e\xb6'), (b'p', b'\xe5\x8f\x91\xe5\xb8\x83')]),
        ),
    ]
