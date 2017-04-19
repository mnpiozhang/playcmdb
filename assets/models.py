#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
from business.models import BusinessInfo,ApplicationInfo

class AssetType(models.Model):
    #ex: server router switch or firewall...
    type_name = models.CharField(max_length = 60,verbose_name = u'固定资产类型名称')
    def __unicode__(self):
        return self.type_name
    
class ServerRoom(models.Model):
    room_name = models.CharField(max_length=50,verbose_name = u'机房名称')
    address = models.CharField(max_length=60,verbose_name = u'机房地址')
    def __unicode__(self):
        return self.room_name

class SystemType(models.Model):
    #ex: centos6.8 redhat6.8 exsi cisco...
    type_name = models.CharField(max_length = 60,verbose_name = u'系统类型名称')
    def __unicode__(self):
        return self.type_name

STATUS_CHOICES = (
                  ('d','下架'),
                  ('p','发布'),
                    )

class AssetInfo(models.Model):
    asset_name = models.CharField(max_length = 40,unique=True,verbose_name = u'设备名称')
    asset_type = models.ForeignKey('AssetType',verbose_name = u'资产类型')
    system_type = models.ForeignKey('SystemType',verbose_name = u'系统类型')
    machine_type = models.CharField(max_length = 40,verbose_name = u'设备位数')
    product = models.CharField(max_length = 40,verbose_name = u'产品名称')
    serial_number = models.CharField(max_length = 40,unique=True,verbose_name = u'设备序列号')
    timestamp = models.DateTimeField(auto_now_add = True,verbose_name = u'创建时间')
    last_modified = models.DateTimeField(auto_now = True,verbose_name = u'最后修改时间')
    location = models.ForeignKey('ServerRoom',verbose_name = u'资产所在位置')
    rack = models.CharField(max_length=20,verbose_name = u'机架位置')
    size = models.CharField(max_length=20,verbose_name = u'尺寸')
    ip = models.CharField(max_length = 20,unique=True,verbose_name = u'IP地址')
    mac = models.CharField(max_length = 20,verbose_name = u'MAC地址')
    memery_size = models.CharField(max_length = 20,verbose_name = u'内存')
    cpu = models.CharField(max_length = 20,verbose_name = u'cpu型号')
    cpu_cores = models.CharField(max_length = 10,verbose_name = u'cpucore数量')
    cpu_pyhsical = models.CharField(max_length = 10,verbose_name = u'cpu物理数量')
    business = models.ManyToManyField(BusinessInfo,related_name='asset_business',verbose_name = u'归属的业务条线')
    app = models.ManyToManyField(ApplicationInfo,related_name='asset_application',verbose_name = u'部署的应用')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='d')
    def __unicode__(self):
        return self.asset_name