#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""playcmdbLTE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import index,delasset,details,submit_asset,edit_asset,virtual_index,submit_virtual,delvirtual,details_vm,edit_vm
from .views import datacenter_index,submit_dc,deldc,details_dc,edit_dc

urlpatterns = [
               url(r'^index/(\d*)', index),
               url(r'^virtual/(\d*)', virtual_index),
               url(r'^datacenter/$',datacenter_index),
               url(r'^del/(?P<id>\w+)/$',delasset),
               url(r'^del_vm/(?P<id>\w+)/$',delvirtual),
               url(r'^del_dc/(?P<id>\w+)/$',deldc),
               url(r'^details/(?P<id>\w+)/$',details),
               url(r'^details_vm/(?P<id>\w+)/$',details_vm),
               url(r'^details_dc/(?P<id>\w+)/$',details_dc),
               url(r'^editasset/(?P<id>\w+)/$',edit_asset),
               url(r'^editvm/(?P<id>\w+)/$',edit_vm),
               url(r'^editdc/(?P<id>\w+)/$',edit_dc),
               url(r'^newasset/$',submit_asset),
               url(r'^newvirtual/$',submit_virtual),
               url(r'^newdc/$',submit_dc),
]
