# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_remove_applicationinfo_business'),
        ('assets', '0005_assetinfo_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMachineInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('virtual_name', models.CharField(unique=True, max_length=40, verbose_name='\u865a\u62df\u8bbe\u5907\u540d\u79f0')),
                ('machine_type', models.CharField(max_length=40, verbose_name='\u865a\u62df\u8bbe\u5907\u4f4d\u6570')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('ip', models.CharField(unique=True, max_length=20, verbose_name='IP\u5730\u5740')),
                ('mac', models.CharField(max_length=20, verbose_name='MAC\u5730\u5740')),
                ('memery_size', models.CharField(max_length=20, verbose_name='\u5185\u5b58')),
                ('cpu', models.CharField(max_length=20, verbose_name='cpu\u578b\u53f7')),
                ('cpu_cores', models.CharField(max_length=10, verbose_name='cpucore\u6570\u91cf')),
                ('cpu_pyhsical', models.CharField(max_length=10, verbose_name='cpu\u7269\u7406\u6570\u91cf')),
                ('status', models.CharField(default=b'd', max_length=1, choices=[(b'd', b'\xe4\xb8\x8b\xe6\x9e\xb6'), (b'p', b'\xe5\x8f\x91\xe5\xb8\x83')])),
                ('app', models.ManyToManyField(related_name='virtual_application', verbose_name='\u90e8\u7f72\u7684\u5e94\u7528', to='business.ApplicationInfo')),
                ('business', models.ManyToManyField(related_name='virtual_business', verbose_name='\u5f52\u5c5e\u7684\u4e1a\u52a1\u6761\u7ebf', to='business.BusinessInfo')),
                ('host', models.ForeignKey(verbose_name='\u5bbf\u4e3b\u673a', to='assets.AssetInfo')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=60, verbose_name='\u865a\u62df\u8bbe\u5907\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='virtualmachineinfo',
            name='virtual_type',
            field=models.ForeignKey(verbose_name='\u865a\u62df\u8bbe\u5907\u7c7b\u578b', to='assets.VirtualType'),
        ),
    ]
