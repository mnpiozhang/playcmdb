#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from accounts.decorators import api_auth
import datetime
from assets.models import AssetInfo
from django.db.models import Q
from django.core import serializers
# Create your views here.

'''
r = requests.get("http://127.0.0.1:8000/api/assets_list/?searchip=1.1.1.12",headers=headers)
r.text
headers
{'Account-ID': 'aaa', 'Authorization': 'f7a9e24777ec23212c54d7a350bc5bea5477fdbb'}
'''
@api_auth
def assets_list(request):
    if request.method == 'GET':
        searchasset = request.GET.get('searchasset',"")
        searchsn = request.GET.get('searchsn',"")
        searchpublish = request.GET.get('searchpublish',"")
        searchip = request.GET.get('searchip',"")
        tmpstarttime = request.GET.get('searchstarttime',"")
        tmpendtime = request.GET.get('searchendtime',"")
    
        if searchpublish == "all":
            tmpstatus = ""
        else:
            tmpstatus = searchpublish
        #判断是否输入了开始时间，没输入或输入非法则默认为1970.01.01
        try:
            searchstarttime = datetime.datetime.strptime(tmpstarttime,'%m/%d/%Y')
        except:
            searchstarttime = datetime.datetime(1970, 1, 1)
        #判断是否输入了结束时间或输入非法，没输入或输入非法则默认为现在
        try:
            searchendtime = datetime.datetime.strptime(tmpendtime,'%m/%d/%Y')
        except:
            searchendtime = datetime.datetime.now()
        #print searchendtime
        allAsset = AssetInfo.objects.filter(Q(ip__contains=searchip)
                                            &Q(asset_name__contains=searchasset)
                                            &Q(status__contains=tmpstatus)
                                            &Q(serial_number__contains=searchsn)
                                            &Q(timestamp__gte=searchstarttime)
                                            &Q(timestamp__lte=searchendtime))
        result_to_json = serializers.serialize("json", allAsset)
        #print result_to_json
        return HttpResponse(result_to_json)
    else:
        return HttpResponse("must use get method")

@api_auth
def create_new_room(request):
    pass