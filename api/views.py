#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from accounts.decorators import api_auth


# Create your views here.


@api_auth
def assets_list(request):
    pass

@api_auth
def create_new_room(request):
    pass