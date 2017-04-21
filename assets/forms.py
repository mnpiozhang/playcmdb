#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from .models import AssetInfo
from django.contrib.admin import widgets


class AssetForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetForm,self).__init__(*args, **kwargs)
        self.fields['asset_type'].choices =  list(self.fields["asset_type"].choices)[1:] 
        self.fields['system_type'].choices =  list(self.fields["system_type"].choices)[1:] 
        self.fields['location'].choices =  list(self.fields["location"].choices)[1:] 

    class Meta:
        model = AssetInfo
        fields = ('asset_name','asset_type','system_type','machine_type','product','serial_number','location','rack',
                  'size','ip','mac','memery_size','cpu','cpu_cores','cpu_pyhsical','business','app','status')
        widgets = {
                   'asset_name' : forms.TextInput(attrs={'id':'user-name','class':'tpl-form-input','placeholder':'资产名称必填'}),
                   'asset_type': forms.Select(attrs={'placeholder':'资产类型必填'}),
                   'system_type': forms.Select(attrs={'placeholder':'类型必填'}),
                   'machine_type' : forms.TextInput(attrs={'placeholder':'位数'}),
                   'product' : forms.TextInput(attrs={'placeholder':'产品名称'}),
                   'serial_number' : forms.TextInput(attrs={'placeholder':'序列号'}),
                   'location' : forms.Select(attrs={'placeholder':'位置'}),
                   'rack' : forms.TextInput(attrs={'placeholder':'机架'}),
                   'size' : forms.TextInput(attrs={'placeholder':'尺寸'}),
                   'ip' : forms.TextInput(attrs={'placeholder':'ip地址'}),
                   'mac' : forms.TextInput(attrs={'placeholder':'mac地址'}),
                   'memery_size' : forms.TextInput(attrs={'placeholder':'内存大小'}),
                   'cpu' : forms.TextInput(attrs={'placeholder':'cpu型号'}),
                   'cpu_cores' : forms.TextInput(attrs={'placeholder':'cpu核数'}),
                   'cpu_pyhsical' : forms.TextInput(attrs={'placeholder':'物理cpu数量'}),
                   'business' : forms.CheckboxSelectMultiple(attrs={'placeholder':'归属业务线'}),
                   'app' : forms.SelectMultiple(attrs={'placeholder':'部署的应用'}),
                   'status' : forms.Select(attrs={'placeholder':'状态'}),
                   }
        error_messages = {
                          'asset_name' :{'required':'请输入文档名称'},
                          'asset_type' :{'required':'请简要填写文档描述，并作为第一搜索依据'},
                          'system_type': {'required':'请选择一个文档类型'},
                          }