from django.contrib import admin
from .models import *
# Register your models here.


class CustomizationsAdmin (admin.ModelAdmin):
    list_display=['product']


class CustomizationsInline (admin.TabularInline) :
    model=Customizations
    extra=1

class ProductGalleryInline (admin.TabularInline) :
    model=ProductGallery
    extra=1

class ProductAdmin (admin.ModelAdmin):
    list_display=['product_name','price','category','update_date','is_available']
    inlines=[ProductGalleryInline,CustomizationsInline]

class ReviewRatingAdmin (admin.ModelAdmin):
    list_display=['user','product','rating','status','updated_at']

class ColorAdmin (admin.ModelAdmin):
    list_display=['color_bg','color_name','color_name_ar']


class CategoryAdmin (admin.ModelAdmin):
    list_display=['category_name','category_name_ar']

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Customizations,CustomizationsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ReviewRating,ReviewRatingAdmin)
admin.site.register(Color_List,ColorAdmin)
admin.site.register(Size_List)

