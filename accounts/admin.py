from django.contrib import admin

# Register your models here.
from .models import UserInfo,UserType
# Register your models here.
admin.site.register(UserType) 
admin.site.register(UserInfo)