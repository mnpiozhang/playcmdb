#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models


# Create your models here.
class BusinessInfo(models.Model):
    business_name = models.CharField(max_length=50,verbose_name = u'业务条线')
    def __unicode__(self):
        return self.business_name
    
    
class ApplicationInfo(models.Model):
    app_name = models.CharField(max_length=50,verbose_name = u'应用名称')
    #business = models.ManyToManyField('BusinessInfo',verbose_name = u'归属的业务条线')
    def __unicode__(self):
        return self.app_name