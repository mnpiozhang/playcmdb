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
import accounts
import assets
import dashboard
from accounts.views import login

#保证admin的时间控件可以用，默认时需要登录admin用户后才能使用，不然使用时会因为获取不到token而使用不了，这里使用直接跳过。
def i18n_javascript(request):
    return admin.site.i18n_javascript(request)

urlpatterns = [
    url(r'^admin/jsi18n', i18n_javascript),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^assets/', include('assets.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^$', login),
]
