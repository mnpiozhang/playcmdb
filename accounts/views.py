#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from .decorators import is_login_auth
import hashlib
from assets.utils import audit_record_login,audit_record_logout,audit_record_change
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
                UserObj = UserInfoObj_form.save()
                audit_record_change(request,UserObj.username,"account")
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
def audit_info(request,id):
    pass