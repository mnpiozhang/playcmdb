# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation', models.CharField(max_length=20, verbose_name='\u64cd\u4f5c')),
                ('target', models.CharField(max_length=30, verbose_name='\u64cd\u4f5c\u76ee\u6807')),
                ('account', models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u6237', to='accounts.UserInfo')),
            ],
        ),
    ]
