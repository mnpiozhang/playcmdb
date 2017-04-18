# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('realname', models.CharField(max_length=20, verbose_name='\u771f\u5b9e\u59d3\u540d')),
                ('telphone', models.CharField(max_length=12, verbose_name='\u7528\u6237\u7535\u8bdd')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=50, verbose_name='\u7528\u6237\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='type',
            field=models.ForeignKey(verbose_name='\u7528\u6237\u7c7b\u578b', to='accounts.UserType'),
        ),
    ]
