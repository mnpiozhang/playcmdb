# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=50, verbose_name='\u5e94\u7528\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_name', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1\u6761\u7ebf')),
            ],
        ),
        migrations.AddField(
            model_name='applicationinfo',
            name='business',
            field=models.ManyToManyField(to='business.BusinessInfo', verbose_name='\u5f52\u5c5e\u7684\u4e1a\u52a1\u6761\u7ebf'),
        ),
    ]
