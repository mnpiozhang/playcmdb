#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from django.shortcuts import redirect,HttpResponse
from .models import UserInfo
# Create decorators
#登录验证装饰器，失败则跳转至登录页面
def is_login_auth(view_func):
    @wraps(view_func)
    def wrapper(request,*args, **kwargs):
        if  request.session.get('login_auth',False):
            return view_func(request,*args, **kwargs)
        else:
            return redirect('/accounts/login/')
    return wrapper

#webshell终端连接验证装饰器，非admin用户无法执行
def is_admin_auth(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        userauth = UserInfo.objects.get(username=request.session.get('username',None)).type.typename
        #print userauth
        #print type(userauth)
        if userauth == "admin":
            return view_func(request,*args, **kwargs)
        else:
            return HttpResponse("usertype is not admin , you have no permission to link remote host")
    return wrapper

'''
请求规则，请求中添加以下两个http请求头
Authorization 加密后的字符串 为用户密码 + 用户名 做 sha1加密运算后的字符串
Account-ID 用户username
'''
#api接口认证
def api_auth(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        '''
        for k,v in request.META.items():
            print k , v
        
        django中http头会进行转换，会将自己添加的http请求头大写并前面增加大写HTTP_ 例如
        Authorization 请求 转换为 HTTP_AUTHORIZATION
        Account-ID 请求 转换为 HTTP_ACCOUNT_ID
        '''
        token = request.META.get('HTTP_AUTHORIZATION', 'unknown')
        username = request.META.get('HTTP_ACCOUNT_ID', 'unknown')
        print token
        print username
        
        if token == 'unknown' or username == 'unknown':
            return HttpResponse("auth fail")
        else:
            try:
                userauth = UserInfo.objects.get(username=username)
                password = userauth.password
                if token == password:
                    return HttpResponse("auth ok")
                else:
                    return HttpResponse("auth fail")
            except:
                return HttpResponse("auth fail")
    return wrapper