from django.contrib import admin

# Register your models here.
from .models import AssetInfo,AssetType,ServerRoom,SystemType
# Register your models here.
admin.site.register(AssetInfo) 
admin.site.register(AssetType)
admin.site.register(ServerRoom)
admin.site.register(SystemType)