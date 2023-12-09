from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class AccountsAdmin (admin.ModelAdmin):
    ordering=['-dete_joined']
    list_display=['full_name','email','last_login','is_active']
    search_fields=['email','username']

class UserProfileAdmin (admin.ModelAdmin):
    
    list_display=['image_tag','user','city','state','country']


admin.site.register(Accounts,AccountsAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
