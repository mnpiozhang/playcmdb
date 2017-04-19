#!/usr/bin/env python
# -*- coding:utf-8 -*-
from accounts.decorators import is_login_auth
from django.shortcuts import render,render_to_response,HttpResponse
import datetime
from .models import AssetInfo
from django.db.models import Q
from .utils import Page,page_div,query_page_div
from accounts.models import UserInfo
from django.template.context import RequestContext

# Create your views here.
@is_login_auth
def index(request,page=1):
    #return render(request, 'assets/index.html', {'a' : "asd"})
    ret = {'AssetObjs':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    if request.method == 'GET':
        #查询页面的分页显示
        if request.GET.get('issearch',None):
            searchasset = request.GET.get('searchasset',None)
            searchsn = request.GET.get('searchsn',None)
            searchpublish = request.GET.get('searchpublish',None)
            searchip = request.GET.get('searchip',None)
            tmpstarttime = request.GET.get('searchstarttime',None)
            tmpendtime = request.GET.get('searchendtime',None)
            Qset = {}
            Qset['searchasset'] = searchasset
            Qset['searchsn'] = searchsn
            Qset['searchpublish'] = searchpublish
            Qset['searchip'] = searchip
            Qset['tmpstarttime'] = tmpstarttime
            Qset['tmpendtime'] = tmpendtime

            #判断是否输入了开始时间，没输入或输入非法则默认为1970.01.01
            try:
                searchstarttime = datetime.datetime.strptime(tmpstarttime,'%Y-%m-%d')
            except:
                searchstarttime = datetime.datetime(1970, 1, 1)
            #判断是否输入了结束时间或输入非法，没输入或输入非法则默认为现在
            try:
                searchendtime = datetime.datetime.strptime(tmpendtime,'%Y-%m-%d')
            except:
                searchendtime = datetime.datetime.now()
            allAsset = AssetInfo.objects.filter(Q(ip__contains=searchip)
                                                &Q(asset_name__contains=searchasset)
                                                &Q(status__contains=searchpublish)
                                                &Q(serial_number__contains=searchsn)
                                                &Q(timestamp__gte=searchstarttime)
                                                &Q(timestamp__lte=searchendtime))
            AllCount = allAsset.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            AssetObjs = allAsset[PageObj.begin:PageObj.end]
            pageurl = 'index'
            app = 'assets'
            querycondition = request.META.get("QUERY_STRING",None)
            pageinfo = query_page_div(page, PageObj.all_page_count,app,pageurl,querycondition)
            ret['PageInfo'] = pageinfo
            ret['AssetObjs'] = AssetObjs
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            ret['Qset'] = Qset
            return render_to_response('assets/index.html',ret,context_instance=RequestContext(request))
        #正常主页的分页显示
        else:
            allAsset = AssetInfo.objects.all()
            AllCount = allAsset.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            AssetObjs = allAsset[PageObj.begin:PageObj.end]
            pageurl = 'index'
            app = 'assets'
            pageinfo = page_div(page, PageObj.all_page_count,app,pageurl)
            ret['PageInfo'] = pageinfo
            ret['AssetObjs'] = AssetObjs
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            return render_to_response('assets/index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponse("this is a web page , please use metod GET")