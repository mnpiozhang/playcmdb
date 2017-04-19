from django.contrib import admin

# Register your models here.
from .models import BusinessInfo,ApplicationInfo
# Register your models here.
admin.site.register(BusinessInfo) 
admin.site.register(ApplicationInfo)