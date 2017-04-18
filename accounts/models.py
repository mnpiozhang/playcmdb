#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
import hashlib

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=50,verbose_name = u'用户名')
    password = models.CharField(max_length=50,verbose_name = u'密码')
    type = models.ForeignKey('UserType',verbose_name = u'用户类型')
    realname = models.CharField(max_length=20,verbose_name = u'真实姓名')
    telphone = models.CharField(max_length=12,verbose_name = u'用户电话')
    def save(self,*args,**kwargs):
        self.password = hashlib.sha1(self.password+self.username).hexdigest()
        super(UserInfo,self).save(*args,**kwargs)
    def __unicode__(self):
        return self.realname
    
class UserType(models.Model):
    typename= models.CharField(max_length=50,verbose_name = u'用户类型名称')
    def __unicode__(self):
        return self.typename