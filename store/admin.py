from django.contrib import admin
from .models import *
# Register your models here.


class ColorAdmin (admin.ModelAdmin):
    prepopulated_fields={'slug':('color_name',)}
    list_display=['color_name','slug']

class SizeAdmin (admin.ModelAdmin):
    prepopulated_fields={'slug':('size_name',)}
    list_display=['size_name','slug']

class ProductGalleryInline (admin.TabularInline) :
    model=ProductGallery
    extra=1

class ProductAdmin (admin.ModelAdmin):
    list_display=['product_name','price',]
    inlines=[ProductGalleryInline]


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Category)
admin.site.register(Favorite)