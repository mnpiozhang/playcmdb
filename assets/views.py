#!/usr/bin/env python
# -*- coding:utf-8 -*-
from accounts.decorators import is_login_auth
from django.shortcuts import render

# Create your views here.
@is_login_auth
def index(request):
    return render(request, 'assets/index.html', {'a' : "asd"})