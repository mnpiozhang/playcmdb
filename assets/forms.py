#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from .models import AssetInfo,VirtualMachineInfo,BusinessInfo,ApplicationInfo,ServerRoom
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
                   'asset_name' : forms.TextInput(attrs={'id':'user-name','class':'form-control','placeholder':'资产名称必填'}),
                   'asset_type': forms.Select(attrs={'placeholder':'资产类型必填','class':'form-control'}),
                   'system_type': forms.Select(attrs={'placeholder':'类型必填','class':'form-control'}),
                   'machine_type' : forms.TextInput(attrs={'placeholder':'位数','class':'form-control'}),
                   'product' : forms.TextInput(attrs={'placeholder':'产品名称','class':'form-control'}),
                   'serial_number' : forms.TextInput(attrs={'placeholder':'序列号','class':'form-control'}),
                   'location' : forms.Select(attrs={'placeholder':'位置','class':'form-control'}),
                   'rack' : forms.TextInput(attrs={'placeholder':'机架','class':'form-control'}),
                   'size' : forms.TextInput(attrs={'placeholder':'尺寸','class':'form-control'}),
                   'ip' : forms.TextInput(attrs={'placeholder':'ip地址','class':'form-control'}),
                   'mac' : forms.TextInput(attrs={'placeholder':'mac地址','class':'form-control'}),
                   'memery_size' : forms.TextInput(attrs={'placeholder':'内存大小','class':'form-control'}),
                   'cpu' : forms.TextInput(attrs={'placeholder':'cpu型号','class':'form-control'}),
                   'cpu_cores' : forms.TextInput(attrs={'placeholder':'cpu核数','class':'form-control'}),
                   'cpu_pyhsical' : forms.TextInput(attrs={'placeholder':'物理cpu数量','class':'form-control'}),
                   'business' : forms.CheckboxSelectMultiple(attrs={'placeholder':'归属业务线','class':'form-control'}),
                   'app' : forms.SelectMultiple(attrs={'placeholder':'部署的应用','class':'form-control'}),
                   'status' : forms.Select(attrs={'placeholder':'状态','class':'form-control'}),
                   }
        error_messages = {
                          'asset_name' :{'required':'请输入文档名称'},
                          'asset_type' :{'required':'请简要填写文档描述，并作为第一搜索依据'},
                          'system_type': {'required':'请选择一个文档类型'},
                          }


class VirtualForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VirtualForm,self).__init__(*args, **kwargs)
        self.fields['virtual_type'].choices =  list(self.fields["virtual_type"].choices)[1:] 
        self.fields['host'].choices =  list(self.fields["host"].choices)[1:] 
        #self.fields['location'].choices =  list(self.fields["location"].choices)[1:] 

    class Meta:
        model = VirtualMachineInfo
        fields = ('virtual_name','virtual_type','machine_type','ip','mac','memery_size','cpu','cpu_cores',
                  'cpu_pyhsical','business','app','status','host','memery_size')
        widgets = {
                   'virtual_name' : forms.TextInput(attrs={'id':'user-name','class':'tpl-form-input','placeholder':'虚拟设备名称必填'}),
                   'virtual_type': forms.Select(attrs={'placeholder':'虚拟设备类型必填'}),
                   'machine_type' : forms.TextInput(attrs={'placeholder':'位数'}),
                   'ip' : forms.TextInput(attrs={'placeholder':'ip地址'}),
                   'mac' : forms.TextInput(attrs={'placeholder':'mac地址'}),
                   'memery_size' : forms.TextInput(attrs={'placeholder':'内存大小'}),
                   'cpu' : forms.TextInput(attrs={'placeholder':'cpu型号'}),
                   'cpu_cores' : forms.TextInput(attrs={'placeholder':'cpu核数'}),
                   'cpu_pyhsical' : forms.TextInput(attrs={'placeholder':'物理cpu数量'}),
                   'business' : forms.CheckboxSelectMultiple(attrs={'placeholder':'归属业务线'}),
                   'app' : forms.SelectMultiple(attrs={'placeholder':'部署的应用'}),
                   'status' : forms.Select(attrs={'placeholder':'状态'}),
                   'host' : forms.Select(attrs={'placeholder':'宿主机'}),
                   }
        error_messages = {
                          'virtual_name' :{'required':'请输入文档名称'},
                          'virtual_type' :{'required':'请简要填写文档描述，并作为第一搜索依据'},
                          'machine_type': {'required':'请选择一个文档类型'},
                          }
        
class ServerRoomForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServerRoomForm,self).__init__(*args, **kwargs)

    class Meta:
        model = ServerRoom
        fields = ('room_name','address','phone')
        widgets = {
                   'room_name' : forms.TextInput(attrs={'id':'user-name','class':'tpl-form-input','placeholder':'机房名称'}),
                   'phone' : forms.TextInput(attrs={'placeholder':'联系电话'}),
                   'address' : forms.TextInput(attrs={'placeholder':'地址'}),
                   }
        error_messages = {
                          'room_name' :{'required':'请输入机房名称'},
                          'phone' :{'required':'请输入联系电话'},
                          'address': {'required':'请输入地址'},
                          }