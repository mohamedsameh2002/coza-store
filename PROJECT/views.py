from django.shortcuts import render,redirect
from store.models import Product,Favorite



def home (request):
    products=Product.objects.filter(is_available=True).order_by('-update_date')
    if request.user.is_authenticated:
        is_fav=Favorite.objects.filter(user=request.user)
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    else:
        id_products_list=[]

    context={
        'products':products,
        'id_products_list':id_products_list,
    }
    return render(request,'home.html',context)