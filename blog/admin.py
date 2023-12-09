from django.contrib import admin
from.models import *

# Register your models here.



class BlogAdmin (admin.ModelAdmin):
    list_display=['publisher','updated_at']
    prepopulated_fields={'slug':('topic',)}

admin.site.register(Blog,BlogAdmin)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Reply)
admin.site.register(Notification)