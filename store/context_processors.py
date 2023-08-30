from .models import Product,Favorite,ProductGallery
from django.http import JsonResponse
from django.shortcuts import render

def LOOP_PRODUCT_CON (request):
    products=Product.objects.all()
    if request.user.is_authenticated:
        count_fav=Favorite.objects.filter(user=request.user).count()
    else:
        products=None
        count_fav=0

    return dict(products=products,count_fav=count_fav)

