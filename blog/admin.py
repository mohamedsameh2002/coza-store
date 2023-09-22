from django.contrib import admin
from.models import *

# Register your models here.

class TagsInline (admin.TabularInline) :
    model=Tags
    extra=1


class BlogAdmin (admin.ModelAdmin):
    list_display=['publisher','updated_at']
    prepopulated_fields={'slug':('topic',)}
    inlines=[TagsInline]

admin.site.register(Blog,BlogAdmin)
admin.site.register(Category)
admin.site.register(Tags)