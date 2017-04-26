#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo,AuditInfo
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from .decorators import is_login_auth
import hashlib
from assets.utils import audit_record_login,audit_record_logout,audit_record_change,Page,page_div
from .forms import UserInfoForm
from django.template.context_processors import csrf

#登陆
@csrf_exempt
def login(request):
# Create your views here.
    ret = {'status':''}
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        is_not_empty=all([username,password])
        passwdhash = hashlib.sha1(password+username).hexdigest()
        if is_not_empty:
            count = UserInfo.objects.filter(username=username,password=passwdhash).count()
            #判断输入用户名密码OK，则跳转到主页面
            if count == 1:
                request.session['username'] = username
                request.session['login_auth'] = True 
                audit_record_login(request)
                #log.info("user login : {}".format(username))
                return redirect('/assets/index/')
            else:
                ret['status']='username or password is error'
        else:
            ret['status']='can not empty'
    return render_to_response('login.html',ret)

#登出
@is_login_auth
def logout(request):
    #log.info("user logout : {}".format(request.session['username']))
    audit_record_logout(request)
    del request.session['login_auth']
    del request.session['username']
    return redirect("/accounts/login/")


@is_login_auth
def account_info(request):
    ret = {'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'accounts'
    ret['SideSub'] = 'info'
    UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
    ret['UserInfoObj'] = UserInfoObj
    return render_to_response('accounts/info.html',ret)


@is_login_auth
def edit_info(request,uname):
    ret = {'UserInfoObj':None,'Side':None,'SideSub':None}
    #### 边框信息点亮判断
    ret['Side'] = 'accounts'
    ret['SideSub'] = 'info'
    tmpname = request.session.get('username',None)
    if tmpname == uname :
        UserInfoObj = UserInfo.objects.get(username=tmpname)
        if request.method == 'POST':
            UserInfoObj_form = UserInfoForm(data=request.POST,files=request.FILES,instance=UserInfoObj)
            if UserInfoObj_form.is_valid():
                changed_telphone = request.POST.get('telphone',None)
                UserInfoObj.telphone = changed_telphone
                UserInfoObj.savebase()
                #UserObj = UserInfoObj_form.save()
                audit_record_change(request,UserInfoObj.username,"account")
                ret['status'] = '修改成功'
            else:
                ret['status'] = '修改失败'
                ret['form'] = UserInfoObj_form
                ret['UserInfoObj'] = UserInfoObj
                #添加跨站请求伪造的认证
                ret.update(csrf(request))
                return render(request,'accounts/edit_info.html',ret)
                
        UserInfoObj_form = UserInfoForm(instance=UserInfoObj)
        ret['UserInfoObj'] = UserInfoObj
        ret['form'] = UserInfoObj_form
        #添加跨站请求伪造的认证
        ret.update(csrf(request))
        return render_to_response('accounts/edit_info.html',ret)
    else:
        return HttpResponse("you can not edit the info of this user")
        
        
        
@is_login_auth
def audit_info(request,page):
    try:
        page = int(page)
    except Exception:
        page = 1
    ret = {'UserInfoObj':None,'Side':None,'SideSub':None,'AuditInfoObjs':None}
    #### 边框信息点亮判断
    ret['Side'] = 'accounts'
    ret['SideSub'] = 'audit'
    account = request.session.get('username',None)
    allMatchAudit = AuditInfo.objects.filter(account = account).order_by('-timestamp')
    AllCount = allMatchAudit.count()
    ret['AllCount'] = AllCount
    PageObj = Page(AllCount,page,10)
    AuditInfoObjs = allMatchAudit[PageObj.begin:PageObj.end]
    pageurl = 'audit'
    app = 'accounts'
    pageinfo = page_div(page, PageObj.all_page_count,app,pageurl)
    ret['PageInfo'] = pageinfo
    ret['AuditInfoObjs'] = AuditInfoObjs
    return render_to_response('accounts/audit.html',ret)