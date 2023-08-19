from django.shortcuts import render,redirect
from .models import Product,ProductGallery,Favorite
import time
# Create your views here.

def PRODUCTS (request):
    products=Product.objects.all()
    is_fav=Favorite.objects.filter(user=request.user)
    id_products_list=[]
    for i in is_fav:
        get_id=i.product_id
        id_products_list.append(get_id)

    context={
        'products':products,
        'id_products_list':id_products_list,
    }
    return render(request,'store/products.html',context)



def PRODUCT_DETAILS (request,id):

    product=Product.objects.get(id=id)
    product_gallery=ProductGallery.objects.filter(product__id=product.id)
    is_fav=Favorite.objects.filter(user=request.user,product_id=id).exists()

    context={
        'product':product,
        'product_gallery':product_gallery,
        'is_fav':is_fav,
    }
    return render(request,'store/product_details.html',context)

def ADD_FAVORITE (request,prod_id):
    url=request.META.get('HTTP_REFERER')
    is_prod_exist=Favorite.objects.filter(user=request.user,product_id=prod_id).exists()
    if is_prod_exist:
        favorite=Favorite.objects.get(user=request.user,product_id=prod_id)
        favorite.delete()
    else:
        favorite=Favorite.objects.create(user=request.user,product_id=prod_id)
    return redirect (url)



def FAVORITE_PAGE (request):
    favorite=Favorite.objects.filter(user=request.user)
    
    return render (request,'store/favorite.html',{'favorite':favorite})