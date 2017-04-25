#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from .models import UserInfo
from django.contrib.admin import widgets
        
class UserInfoForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserInfoForm,self).__init__(*args, **kwargs)

    class Meta:
        model = UserInfo
        fields = ('telphone',)
        widgets = {
                   'telphone' : forms.TextInput(attrs={'placeholder':'机房名称'}),
                   }
        error_messages = {
                          'telphone' :{'required':'请修改手机号码'},
                          }