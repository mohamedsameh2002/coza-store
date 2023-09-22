from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html

# Register your models here.

class AccountsAdmin (UserAdmin):
    list_display=['email','username','first_name','last_name','last_login','dete_joined','is_active']
    list_display_links=['email','first_name','last_name']
    readonly_fields=['last_login','dete_joined']
    ordering=['-dete_joined']
    filter_horizontal=[]
    list_filter=[]
    fieldsets=[]

class UserProfileAdmin (admin.ModelAdmin):
    
    list_display=['image_tag','user','city','state','country']


admin.site.register(Accounts,AccountsAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
