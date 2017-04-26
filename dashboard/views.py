#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from accounts.decorators import is_login_auth
from assets.utils import audit_record_login,audit_record_logout,audit_record_change,Page,page_div
from django.template.context_processors import csrf
from assets.models import AssetInfo,AssetType,SystemType
from django.db.models import Count

@is_login_auth
def show_dashboard(request):
    ret = {'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'dashboard'
    ret['SideSub'] = 'dashboard'
    #asset_types = AssetInfo.objects.values('asset_type').annotate(num_assettype=Count('asset_type'))
    asset_types = AssetType.objects.all().annotate(num_assettypes=Count('assetinfo'))
    '''
    for i in asset_types:
        print i,i.num_assettypes
    '''
    system_types = SystemType.objects.all().annotate(num_systemtypes=Count('assetinfo'))
    for i  in system_types:
        print i.num_systemtypes
    ret['assettypes'] = asset_types
    ret['systemtypes'] = system_types
    UserInfoObj = request.session.get('username',None)
    ret['UserInfoObj'] = UserInfoObj
    return render_to_response('dashboard/dashboard.html',ret)