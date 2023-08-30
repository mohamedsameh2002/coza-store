from django.shortcuts import render,redirect
from .models import Product,ProductGallery,Favorite,Category,Color
import time
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
# Create your views here.

def PRODUCTS (request):
    products=Product.objects.filter(is_available=True).order_by('-update_date')
    category=Category.objects.all()
    colors=Color.objects.all()
    count_products=Product.objects.count()
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
        'category':category,
        'colors':colors,
        'count_products':count_products,
    }
    return render(request,'store/products.html',context)



def QUICK_VIEW (request):
    id=request.GET.get('id')
    product=Product.objects.get(id=id)
    product_gallery=ProductGallery.objects.filter(product__id=product.id)
    sizes=product.sizes.values_list('size_name',flat=True)
    colors=product.colors.values_list('color_name',flat=True)
    data={
        'colors':list (colors),
        'sizes':list (sizes),
    }
    return JsonResponse(data)




def LOAD_MORE (request):
    offset=int (request.GET.get('offist'))
    limit= int (request.GET.get('limit'))
    data=Product.objects.all().order_by('-created_date')[offset:offset+limit]
    t=render_to_string('ajax/product_list.html',{'data':data})
    return JsonResponse({'data':t})



def PRODUCT_DETAILS (request,id):
    product=Product.objects.get(id=id)
    products=Product.objects.filter(is_available=True).order_by('-update_date')
    product_gallery=ProductGallery.objects.filter(product__id=product.id)
    sizes=product.sizes.values_list('size_name',flat=True)
    colors=product.colors.values_list('color_name',flat=True)
    if request.user.is_authenticated:
        is_fav=Favorite.objects.filter(user=request.user,product_id=id).exists()
    else :
        is_fav=False

    context={
        'product':product,
        'product_gallery':product_gallery,
        'is_fav':is_fav,
        'sizes':sizes,
        'colors':colors,
        'products':products,
    }
    return render(request,'store/product_details.html',context)

def ADD_FAVORITE (request):
    prod_id=request.GET.get('id')
    url=request.META.get('HTTP_REFERER')
    is_prod_exist=Favorite.objects.filter(user=request.user,product_id=prod_id).exists()
    if is_prod_exist:
        favorite=Favorite.objects.get(user=request.user,product_id=prod_id)
        favorite.delete()
    else:
        favorite=Favorite.objects.create(user=request.user,product_id=prod_id)
    count=Favorite.objects.filter(user=request.user).count()
    return JsonResponse({'data':count})



def FAVORITE_PAGE (request):
    favorite=Favorite.objects.filter(user=request.user)
    
    return render (request,'store/favorite.html',{'favorite':favorite})



def SEARCH (request):
    if 'search' in request.GET:
        search=request.GET['search']
        if search:
            products=Product.objects.filter(Q(description__icontains=search) | Q(product_name__icontains=search)).order_by('-update_date') 
            category=Category.objects.all()
            colors=Color.objects.all()
            count_products=Product.objects.count()
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
        'category':category,
        'colors':colors,
        'count_products':count_products,
    }
    return render (request,'store/search.html',context)