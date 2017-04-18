#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo
from django.shortcuts import redirect,HttpResponse,render_to_response
from .decorators import is_login_auth,is_admin_auth
import hashlib

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
                #log.info("user login : {}".format(username))
                return redirect('/assets/index/')
            else:
                ret['status']='password error'
        else:
            ret['status']='can not empty'
    return render_to_response('login.html',ret)

#登出
@is_login_auth
def logout(request):
    #log.info("user logout : {}".format(request.session['username']))
    del request.session['login_auth']
    del request.session['username']
    return redirect("/web/login/")
