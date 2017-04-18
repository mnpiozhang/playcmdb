# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_name', models.CharField(unique=True, max_length=40, verbose_name='\u8bbe\u5907\u4f4d\u6570')),
                ('machine_type', models.CharField(max_length=40, verbose_name='\u8bbe\u5907\u4f4d\u6570')),
                ('product', models.CharField(max_length=40, verbose_name='\u4ea7\u54c1\u540d\u79f0')),
                ('serial_number', models.CharField(unique=True, max_length=40, verbose_name='\u8bbe\u5907\u5e8f\u5217\u53f7')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('rack', models.CharField(max_length=20, verbose_name='\u673a\u67b6\u4f4d\u7f6e')),
                ('size', models.CharField(max_length=20, verbose_name='\u5c3a\u5bf8')),
                ('ip', models.CharField(unique=True, max_length=20, verbose_name='IP\u5730\u5740')),
                ('memery_size', models.CharField(max_length=20, verbose_name='\u5185\u5b58')),
                ('cpu', models.CharField(max_length=20, verbose_name='cpu\u578b\u53f7')),
                ('cpu_cores', models.CharField(max_length=10, verbose_name='cpucore\u6570\u91cf')),
                ('cpu_pyhsical', models.CharField(max_length=10, verbose_name='cpu\u7269\u7406\u6570\u91cf')),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=60, verbose_name='\u56fa\u5b9a\u8d44\u4ea7\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='ServerRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_name', models.CharField(max_length=50, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('address', models.CharField(max_length=60, verbose_name='\u673a\u623f\u5730\u5740')),
            ],
        ),
        migrations.CreateModel(
            name='SystemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=60, verbose_name='\u7cfb\u7edf\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='assetinfo',
            name='asset_type',
            field=models.ForeignKey(verbose_name='\u8d44\u4ea7\u7c7b\u578b', to='assets.AssetType'),
        ),
        migrations.AddField(
            model_name='assetinfo',
            name='location',
            field=models.ForeignKey(verbose_name='\u8d44\u4ea7\u6240\u5728\u4f4d\u7f6e', to='assets.ServerRoom'),
        ),
        migrations.AddField(
            model_name='assetinfo',
            name='system_type',
            field=models.ForeignKey(verbose_name='\u7cfb\u7edf\u7c7b\u578b', to='assets.SystemType'),
        ),
    ]
