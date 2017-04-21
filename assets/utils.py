#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.utils.safestring import mark_safe
import re
import urllib
from accounts.models import AuditInfo
class Page:
    def __init__(self,AllCount,current_page,datanum=3):
        '''
        AllCount 所有数据条数  int
        current_page 当前页  int 
        datanum 每个页面展示多少条数据 ，默认3条  int
        '''
        self.DataNum=datanum
        self.AllCount=AllCount
        self.CurrentPage=current_page
        
    #装饰器property将方法装饰为属性
    @property
    def begin(self):
        return (self.CurrentPage-1)*self.DataNum
    @property
    def end(self):
        return self.CurrentPage*self.DataNum
    @property
    def all_page_count(self):
        #计算分页页面数量，一共有几页，divmod方法返回商和余数的元祖
        all_page = divmod(self.AllCount,self.DataNum)
        if all_page[1] == 0 and all_page[0] != 0:
            all_page_count = all_page[0]
        else:
            all_page_count = all_page[0]+1
        return all_page_count
        
#正常页面的分页方法        
def page_div(page,all_page_count,app,pageurl):
    '''
    page 总页面分页
    page 当前页面   int
    all_page_count 总页数 int
    app 应用名称 str
    pageurl 分页的页面信息 str
    '''
    #初始化页面分页为列表类型
    pagelist = []
    #分页逻辑判断，html标签的列表
    pagelist.append("<li><a class='pure-button' href='/%s/%s/1'>首页</a></li>" %(app,pageurl))
    if page == 1:
        pagelist.append("<li><a href='#'>上一页</a></li>")
    else:
        pagelist.append("<li><a  class='pure-button prev' href='/%s/%s/%d'>上一页</a></li>" %(app,pageurl,(page-1)))
    
    
    #一次展示9个分页
    if all_page_count < 9:
        begin =0
        end =all_page_count
    elif page <5:
        begin =0
        end =9
        #end = page+4 
    elif page > all_page_count-4:
        #begin = page-5
        begin = all_page_count-9
        end = all_page_count    
    else:
        begin = page-5
        end = page+4
    for i in range(begin,end):
        if page == i+1:
            pagelist.append("<li><a class='pure-button' style='color:red;' href='/%s/%s/%d'>%d</a></li>" %(app,pageurl,i+1,i+1))
        else:
            pagelist.append("<li><a class='pure-button' href='/%s/%s/%d'>%d</a></li>" %(app,pageurl,i+1,i+1))
            

    if page == all_page_count:
        pagelist.append("<li><a class='pure-button next' href='#'>下一页</a></li>")
    else:
        pagelist.append("<li><a class='pure-button next' href='/%s/%s/%d'>下一页</a></li>" %(app,pageurl,(page+1)))
    pagelist.append("<li><a class='pure-button' href='/%s/%s/%d'>尾页</a></li>" %(app,pageurl,all_page_count))
    #将列表类型的页面转换成字符串并且转义html标签能在前台显示
    return mark_safe(' '.join(pagelist))

#查询页面的分页方法        
def query_page_div(page,all_page_count,app,pageurl,querycondition):
    '''
    page 总页面分页
    page 当前页面   int
    all_page_count 总页数 int
    app 应用名称
    pageurl 分页的页面信息 str
    '''
    #初始化页面分页为列表类型
    pagelist = []
    #分页逻辑判断，html标签的列表
    pagelist.append("<li><a class='pure-button' href='/%s/%s/1?%s'>首页</a></li>" %(app,pageurl,querycondition))
    if page == 1:
        pagelist.append("<li><a class='pure-button prev' href='#'>上一页</a></li>")
    else:
        pagelist.append("<li><a  class='pure-button prev' href='/%s/%s/%d?%s'>上一页</a></li>" %(app,pageurl,(page-1),querycondition))
    
    
    #一次展示9个分页
    if all_page_count < 9:
        begin =0
        end =all_page_count
    elif page <5:
        begin =0
        end =9
        #end = page+4 
    elif page > all_page_count-4:
        #begin = page-5
        begin = all_page_count-9
        end = all_page_count    
    else:
        begin = page-5
        end = page+4
    for i in range(begin,end):
        if page == i+1:
            pagelist.append("<li><a class='pure-button' style='color:red;' href='/%s/%s/%d?%s'>%d</a></li>" %(app,pageurl,i+1,querycondition,i+1))
        else:
            pagelist.append("<li><a class='pure-button' href='/%s/%s/%d?%s'>%d</a></li>" %(app,pageurl,i+1,querycondition,i+1))
            

    if page == all_page_count:
        pagelist.append("<li><a class='pure-button next' href='#'>下一页</a></li>")
    else:
        pagelist.append("<li><a class='pure-button next' href='/%s/%s/%d?%s'>下一页</a></li>" %(app,pageurl,(page+1),querycondition))
    pagelist.append("<li><a class='pure-button' href='/%s/%s/%d?%s'>尾页</a></li>" %(app,pageurl,all_page_count,querycondition))
    #将列表类型的页面转换成字符串并且转义html标签能在前台显示
    return mark_safe(' '.join(pagelist))

def audit_record_login(request):
    user = request.session['username']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remote_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:  
        remote_ip = request.META['REMOTE_ADDR']
    operation = "login"
    AuditInfo.objects.create(
                             account = user,
                             operation = operation,
                             remote_ip = remote_ip
                             )
    
def audit_record_logout(request):
    user = request.session['username']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remote_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:  
        remote_ip = request.META['REMOTE_ADDR']
    operation = "logout"
    AuditInfo.objects.create(
                             account = user,
                             operation = operation,
                             remote_ip = remote_ip
                             )

def audit_record_del(request,assertname):
    user = request.session['username']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remote_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:  
        remote_ip = request.META['REMOTE_ADDR']
    operation = "del"
    AuditInfo.objects.create(
                             account = user,
                             operation = operation,
                             remote_ip = remote_ip,
                             target = assertname
                             )
    
def audit_record_create(request,assertname):
    user = request.session['username']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remote_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:  
        remote_ip = request.META['REMOTE_ADDR']
    operation = "create"
    AuditInfo.objects.create(
                             account = user,
                             operation = operation,
                             remote_ip = remote_ip,
                             target = assertname
                             )
    
def audit_record_change(request,assertname):
    user = request.session['username']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remote_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:  
        remote_ip = request.META['REMOTE_ADDR']
    operation = "change"
    AuditInfo.objects.create(
                             account = user,
                             operation = operation,
                             remote_ip = remote_ip,
                             target = assertname
                             )