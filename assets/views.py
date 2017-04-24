#!/usr/bin/env python
# -*- coding:utf-8 -*-
from accounts.decorators import is_login_auth
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import datetime
from django.template.context_processors import csrf
from .models import AssetInfo,VirtualMachineInfo,ServerRoom
from django.db.models import Q
from .utils import Page,page_div,query_page_div,audit_record_del,audit_record_create,audit_record_change
from .forms import AssetForm,VirtualForm,ServerRoomForm
from accounts.models import UserInfo,AuditInfo
from django.template.context import RequestContext

###### asset info view#########
# Create your views here.
@is_login_auth
def index(request,page=1):
    #return render(request, 'assets/index.html', {'a' : "asd"})
    ret = {'AssetObjs':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'index'
    ####
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
            if searchpublish == "all":
                tmpstatus = ""
            else:
                tmpstatus = searchpublish
            Qset['searchip'] = searchip
            Qset['tmpstarttime'] = tmpstarttime
            Qset['tmpendtime'] = tmpendtime
            #print Qset
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
                                                &Q(status__contains=tmpstatus)
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
        return HttpResponse("this is a web page , please use method GET")
    
#删除资产信息信息
@is_login_auth
def delasset(request,id):
    AssetObj = AssetInfo.objects.get(id=id)
    audit_record_del(request,AssetObj.asset_name)
    AssetObj.delete()
    return redirect("/assets/index/")


#显示资产信息详情
@is_login_auth
def details(request,id):
    ret = {'AssetObj':None,'UserInfoObj':None,'Side':None,'SideSub':None,'VmObj':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'index'
    AssetObj = AssetInfo.objects.get(id=id)
    VmObj = VirtualMachineInfo.objects.filter(host = AssetObj)
    ret['VmObj'] = VmObj
    ret['AssetObj'] = AssetObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['id'] = id
    return render_to_response('assets/details.html',ret)
    
#提交新的资产信息
@is_login_auth
def submit_asset(request):
    ret = {'AssetObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'index'
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    if request.method == 'POST':
        AssetObj_form = AssetForm(request.POST)
        #print AssetObj_form
        if AssetObj_form.is_valid():
            AssetObj = AssetObj_form.save()
            #添加记录审计,可以加一些其他操作
            audit_record_create(request,AssetObj.asset_name)
            ret['status'] = 'save ok'
            
        else:
            ret['status'] = 'save error'
            ret['form'] = AssetObj_form
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/submitasset.html',ret)
            
    AssetObj_form = AssetForm()
    ret['form'] = AssetObj_form
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/submitasset.html',ret)

#编辑资产信息
@is_login_auth
def edit_asset(request,id):
    ret = {'AssetObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'index'
    AssetInfoObj = AssetInfo.objects.get(id=id)
    if request.method == 'POST':
        AssetInfoObj_form = AssetForm(data=request.POST,files=request.FILES,instance=AssetInfoObj)
        #print request.POST
        #print request.FILES['attachment'].name
        #print DocumentInfoObj.attachment
        #print str(DocumentInfoObj.attachment)
        #print DocumentInfoObj_form.attachment
        if AssetInfoObj_form.is_valid():
            AssetObj = AssetInfoObj_form.save()
            #AssetObj = AssetInfoObj_form.save(commit=False)
            #print AssetObj.app
            #索引状态放置为b即开始索引
            audit_record_change(request,AssetObj.asset_name)
            #AssetObj.save()
            ret['status'] = '修改成功'
        else:
            ret['status'] = '修改失败'
            ret['form'] = AssetInfoObj_form
            ret['AssetObj'] = AssetInfoObj
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/edit_asset.html',ret)
            
    AssetInfoObj_form = AssetForm(instance=AssetInfoObj)
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['form'] = AssetInfoObj_form
    ret['id'] = id
    ret['AssetObj'] = AssetInfoObj
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/edit_asset.html',ret)


###### virtual info view#########

@is_login_auth
def virtual_index(request,page=1):
    ret = {'VirtualObjs':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'virtual'
    ####
    try:
        page = int(page)
    except Exception:
        page = 1
    if request.method == 'GET':
        #查询页面的分页显示
        if request.GET.get('issearch',None):
            searchvirtual = request.GET.get('searchvirtual',None)
            searchpublish = request.GET.get('searchpublish',None)
            searchip = request.GET.get('searchip',None)
            tmpstarttime = request.GET.get('searchstarttime',None)
            tmpendtime = request.GET.get('searchendtime',None)
            Qset = {}
            Qset['searchvirtual'] = searchvirtual
            Qset['searchpublish'] = searchpublish
            if searchpublish == "all":
                tmpstatus = ""
            else:
                tmpstatus = searchpublish
            Qset['searchip'] = searchip
            Qset['tmpstarttime'] = tmpstarttime
            Qset['tmpendtime'] = tmpendtime
            #print Qset
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
            allVirtual = VirtualMachineInfo.objects.filter(Q(ip__contains=searchip)
                                                         &Q(virtual_name__contains=searchvirtual)
                                                         &Q(status__contains=tmpstatus)
                                                         &Q(timestamp__gte=searchstarttime)
                                                         &Q(timestamp__lte=searchendtime))
            AllCount = allVirtual.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            VirtualObjs = allVirtual[PageObj.begin:PageObj.end]
            pageurl = 'virtual'
            app = 'assets'
            querycondition = request.META.get("QUERY_STRING",None)
            pageinfo = query_page_div(page, PageObj.all_page_count,app,pageurl,querycondition)
            ret['PageInfo'] = pageinfo
            ret['VirtualObjs'] = VirtualObjs
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            ret['Qset'] = Qset
            return render_to_response('assets/virtual_index.html',ret,context_instance=RequestContext(request))
        #正常主页的分页显示
        else:
            allVirtual = VirtualMachineInfo.objects.all()
            AllCount = allVirtual.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            VirtualObjs = allVirtual[PageObj.begin:PageObj.end]
            pageurl = 'virtual'
            app = 'assets'
            pageinfo = page_div(page, PageObj.all_page_count,app,pageurl)
            ret['PageInfo'] = pageinfo
            ret['VirtualObjs'] = VirtualObjs
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            return render_to_response('assets/virtual_index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponse("this is a web page , please use method GET")
    
    
#提交新的虚拟化信息
@is_login_auth
def submit_virtual(request):
    ret = {'VirtualObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'virtual'
    #print "12312"
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    if request.method == 'POST':
        VirtualObj_form = VirtualForm(request.POST)
        #print VirtualObj_form
        if VirtualObj_form.is_valid():
            VirtualObj = VirtualObj_form.save()
            #添加记录审计,可以加一些其他操作
            audit_record_create(request,VirtualObj.virtual_name)
            ret['status'] = 'save ok'
            
        else:
            ret['status'] = 'save error'
            ret['form'] = VirtualObj_form
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/submitvirtual.html',ret)
            
    VirtualObj_form = VirtualForm()
    ret['form'] = VirtualObj_form
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/submitvirtual.html',ret)

#删除虚拟化信息
@is_login_auth
def delvirtual(request,id):
    VirtualObj = VirtualMachineInfo.objects.get(id=id)
    audit_record_del(request,VirtualObj.virtual_name)
    VirtualObj.delete()
    return redirect("/assets/virtual/")

#显示资产信息详情
@is_login_auth
def details_vm(request,id):
    ret = {'VirtualObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'virtual'
    VirtualObj = VirtualMachineInfo.objects.get(id=id)
    ret['VirtualObj'] = VirtualObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['id'] = id
    return render_to_response('assets/virtual_details.html',ret)

#编辑虚拟化信息
@is_login_auth
def edit_vm(request,id):
    ret = {'VirtualObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'virtual'
    VirtualInfoObj = VirtualMachineInfo.objects.get(id=id)
    if request.method == 'POST':
        VirtualInfoObj_form = VirtualForm(data=request.POST,files=request.FILES,instance=VirtualInfoObj)
        #print request.POST
        #print request.FILES['attachment'].name
        #print DocumentInfoObj.attachment
        #print str(DocumentInfoObj.attachment)
        #print DocumentInfoObj_form.attachment
        if VirtualInfoObj_form.is_valid():
            VirtualObj = VirtualInfoObj_form.save()
            #AssetObj = AssetInfoObj_form.save(commit=False)
            #print AssetObj.app
            #索引状态放置为b即开始索引
            audit_record_change(request,VirtualObj.virtual_name)
            #AssetObj.save()
            ret['status'] = '修改成功'
        else:
            ret['status'] = '修改失败'
            ret['form'] = VirtualInfoObj_form
            ret['VirtualObj'] = VirtualInfoObj
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/edit_vm.html',ret)
            
    VirtualInfoObj_form = VirtualForm(instance=VirtualInfoObj)
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['form'] = VirtualInfoObj_form
    ret['id'] = id
    ret['VirtualObj'] = VirtualInfoObj
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/edit_vm.html',ret)


######机房信息
@is_login_auth
def datacenter_index(request,page=1):
    ret = {'DCObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    ret['Side'] = 'asset'
    ret['SideSub'] = 'datacenter'
    DCObj = ServerRoom.objects.all()
    ret['DCObj'] = DCObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    return render(request,'assets/dc_index.html',ret)

@is_login_auth
def submit_dc(request):
    ret = {'DCObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'datacenter'
    #print "12312"
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    if request.method == 'POST':
        DCObj_form = ServerRoomForm(request.POST)
        #print VirtualObj_form
        if DCObj_form.is_valid():
            DCObj = DCObj_form.save()
            #添加记录审计,可以加一些其他操作
            audit_record_create(request,DCObj.room_name)
            ret['status'] = 'save ok'
            
        else:
            ret['status'] = 'save error'
            ret['form'] = DCObj_form
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/submitdc.html',ret)
            
    DCObj_form = ServerRoomForm()
    ret['form'] = DCObj_form
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/submitdc.html',ret)

#删除机房
@is_login_auth
def deldc(request,id):
    DCObj = ServerRoom.objects.get(id=id)
    audit_record_del(request,DCObj.room_name)
    DCObj.delete()
    return redirect("/assets/datacenter/")

#显示机房的信息详情
@is_login_auth
def details_dc(request,id):
    ret = {'DCObj':None,'UserInfoObj':None,'Side':None,'SideSub':None,'AssetsObj':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'datacenter'
    DCObj = ServerRoom.objects.get(id=id)
    ret['DCObj'] = DCObj
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['id'] = id
    AssetsObj = AssetInfo.objects.filter(location=DCObj)
    ret['AssetsObj'] = AssetsObj
    return render_to_response('assets/dc_details.html',ret)

@is_login_auth
def edit_dc(request,id):
    ret = {'DCObj':None,'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'asset'
    ret['SideSub'] = 'datacenter'
    DCInfoObj = ServerRoom.objects.get(id=id)
    if request.method == 'POST':
        DCInfoObj_form = ServerRoomForm(data=request.POST,files=request.FILES,instance=DCInfoObj)
        #print request.POST
        #print request.FILES['attachment'].name
        #print DocumentInfoObj.attachment
        #print str(DocumentInfoObj.attachment)
        #print DocumentInfoObj_form.attachment
        if DCInfoObj_form.is_valid():
            DCObj = DCInfoObj_form.save()
            #AssetObj = AssetInfoObj_form.save(commit=False)
            #print AssetObj.app
            #索引状态放置为b即开始索引
            audit_record_change(request,DCObj.room_name)
            #AssetObj.save()
            ret['status'] = '修改成功'
        else:
            ret['status'] = '修改失败'
            ret['form'] = DCInfoObj_form
            ret['DCObj'] = DCInfoObj
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'assets/edit_dc.html',ret)
            
    DCInfoObj_form = ServerRoomForm(instance=DCInfoObj)
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    ret['form'] = DCInfoObj_form
    ret['id'] = id
    ret['DCObj'] = DCInfoObj
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('assets/edit_dc.html',ret)