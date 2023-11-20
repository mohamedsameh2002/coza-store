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


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Customizations,CustomizationsAdmin)
admin.site.register(Category)
admin.site.register(ReviewRating,ReviewRatingAdmin)
admin.site.register(Color_List)
admin.site.register(Size_List)

