from django.shortcuts import render,redirect
from .models import Product,ProductGallery,Favorite,Category,Color,Size
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import string
import random
import secrets
# Create your views here.

def _favorit_id (request):
    favorit=request.session.session_key
    if not favorit :
        favorit=request.session.create()
    return favorit

def PRODUCTS (request):
    products=Product.objects.filter(is_available=True).order_by('-update_date')[:1]
    category=Category.objects.all()
    colors=Color.objects.all()
    sizes=Size.objects.all()
    count_products=Product.objects.count()
    if request.user.is_authenticated:
        is_fav=Favorite.objects.filter(user=request.user)
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    else:
        is_fav=Favorite.objects.filter(by_session=_favorit_id(request))
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)

    context={
        'products':products,
        'id_products_list':id_products_list,
        'category':category,
        'colors':colors,
        'sizes':sizes,
        'count_products':count_products,
    }
    return render(request,'store/products.html',context)



def QUICK_VIEW (request):
    id=request.GET.get('id')
    product=Product.objects.get(id=id)
    sizes=product.sizes.values_list('size_name',flat=True)
    colors=product.colors.values_list('color_name',flat=True)
    data={
        'colors':list (colors),
        'sizes':list (sizes),
    }
    return JsonResponse(data)


def LOAD_MORE(request):
    colors=request.GET.getlist('_filterObj[color][]')
    sizes=request.GET.getlist('_filterObj[size][]')
    categorys=request.GET.getlist('_filterObj[category][]')
    offset=int(request.GET['offset'])#اللي موجود دلوقت ف الصفحه
    limit=int(request.GET['limit'])# اللي انا عينته عند الزرار 
    minPrice=request.GET['_filterObj[minPrice]']
    maxPrice=request.GET['_filterObj[maxPrice]']
    storby=request.GET.getlist('_filterObj[storby][]')
    # creat random class
    # all_chars = string.ascii_letters + string.digits 
    # serial_list = [random.choice(all_chars) for _ in range(8)]
    # serial_string = ''.join(serial_list)
    random_1_fvort = secrets.token_hex(4).title().swapcase()
    random_2_qick = secrets.token_hex(4).title().swapcase()
    random_3_addmodal = secrets.token_hex(4).title().swapcase()
    #===================
    products=Product.objects.filter(is_available=True).order_by('-update_date').distinct()
    products=products.filter(price__gte=minPrice)
    products=products.filter(price__lte=maxPrice)
    
    if colors or sizes or categorys:
        if len(colors) > 0 and len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(colors__id__in=colors,sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct()[offset:offset+limit]


        elif  len(colors) > 0 and len(sizes) > 0 :
            x=products.filter(colors__id__in=colors,sizes__id__in=sizes).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,sizes__id__in=sizes).order_by('-update_date').distinct()[offset:offset+limit]



        elif len(colors) > 0  and len(categorys) > 0 :
            x=products.filter(colors__id__in=colors,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,category__id__in=categorys).order_by('-update_date').distinct()[offset:offset+limit]


        elif  len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct()[offset:offset+limit]

            
        else  :
            if len(colors) > 0:
                x=products.filter(colors__id__in=colors).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(colors__id__in=colors).order_by('-update_date').distinct()[offset:offset+limit]

            elif len(sizes) > 0:
                x=products.filter(sizes__id__in=sizes).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(sizes__id__in=sizes).order_by('-update_date').distinct()[offset:offset+limit]

            elif  len(categorys) > 0:
                x=products.filter(category__id__in=categorys).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(category__id__in=categorys).order_by('-update_date').distinct()[offset:offset+limit]

    else:
        count=products.filter(is_available=True).distinct().count()

        if storby :
            if storby == ['1']:
                products=products.filter(is_available=True).distinct()[offset:offset+limit]
            elif storby == ['2']:
                products=products.filter(is_available=True).order_by('product_name').distinct()[offset:offset+limit]
            elif storby == ['3']:
                products=products.filter(is_available=True).order_by('-product_name').distinct()[offset:offset+limit]
            elif storby == ['4']:#th reat
                products=products.filter(is_available=True).order_by('-product_name').distinct()[offset:offset+limit]
            elif storby == ['5']:
                products=products.filter(is_available=True).order_by('created_date').distinct()[offset:offset+limit]
            elif storby == ['6']:
                products=products.filter(is_available=True).order_by('price').distinct()[offset:offset+limit]
            elif storby == ['7']:
                products=products.filter(is_available=True).order_by('-price').distinct()[offset:offset+limit]
        else:
            products=products.filter(is_available=True).order_by('-update_date').distinct()[offset:offset+limit]








#==============================================================
    if request.user.is_authenticated:
        is_fav=Favorite.objects.filter(user=request.user)
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    else:
        is_fav=Favorite.objects.filter(by_session=_favorit_id(request))
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    context={
        'products':products,
        'id_products_list':id_products_list,
        'random_1_fvort':random_1_fvort,
        'random_2_qick':random_2_qick,
        'random_3_addmodal':random_3_addmodal,
    }
    t=render_to_string('ajax/products_loadmore.html',context)
    return JsonResponse({'data':t,'count':count})


def PRODUCT_DETAILS (request,id):
    product=Product.objects.get(id=id)
    catigory=product.category
    products=Product.objects.filter(is_available=True,category=catigory).exclude(id=id).order_by('-update_date')
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
    if request.user.is_authenticated:
        prod_id=request.GET.get('id')
        url=request.META.get('HTTP_REFERER')
        is_prod_exist=Favorite.objects.filter(user=request.user,product_id=prod_id).exists()
        if is_prod_exist:
            favorite=Favorite.objects.get(user=request.user,product_id=prod_id)
            favorite.delete()
        else:
            favorite=Favorite.objects.create(user=request.user,product_id=prod_id)
        count=Favorite.objects.filter(user=request.user).count()
        favorite=Favorite.objects.filter(user=request.user)
    else:
        prod_id=request.GET.get('id')
        is_prod_exist=Favorite.objects.filter(by_session=_favorit_id(request),product_id=prod_id).exists()
        if is_prod_exist:
            favorite=Favorite.objects.get(by_session=_favorit_id(request),product_id=prod_id)
            favorite.delete()
        else:
            favorite=Favorite.objects.create(by_session=_favorit_id(request),product_id=prod_id)
        count=Favorite.objects.filter(by_session=_favorit_id(request)).count()
        favorite=Favorite.objects.filter(by_session=_favorit_id(request))


    template=render_to_string('ajax/favorit_aj.html',{'favorite':favorite})
    template_2=render_to_string('ajax/favorit_imty_aj.html')
    data={
        'count':count,
        'template':template,
        'template_2':template_2,
    }
    return JsonResponse(data)



def FAVORITE_PAGE (request):
    if request.user.is_authenticated:
        favorite=Favorite.objects.filter(user=request.user)
    else:
        favorite=Favorite.objects.filter(by_session=_favorit_id(request))

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


def FILTER(request):
    colors=request.GET.getlist('color[]')
    sizes=request.GET.getlist('size[]')
    categorys=request.GET.getlist('category[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    storby=request.GET.getlist('storby[]')
    products=Product.objects.filter(is_available=True).order_by('-update_date').distinct()
    products=products.filter(price__gte=minPrice,price__lte=maxPrice)

    if colors or sizes or categorys:
        if len(colors) > 0 and len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(colors__id__in=colors,sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct()[:1]


        elif  len(colors) > 0 and len(sizes) > 0 :
            x=products.filter(colors__id__in=colors,sizes__id__in=sizes).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,sizes__id__in=sizes).order_by('-update_date').distinct()[:1]



        elif len(colors) > 0  and len(categorys) > 0 :
            x=products.filter(colors__id__in=colors,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(colors__id__in=colors,category__id__in=categorys).order_by('-update_date').distinct()[:1]


        elif  len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct().count()  
            count=x
            products=products.filter(sizes__id__in=sizes,category__id__in=categorys).order_by('-update_date').distinct()[:1]

            
        else  :
            if len(colors) > 0:
                x=products.filter(colors__id__in=colors).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(colors__id__in=colors).order_by('-update_date').distinct()[:1] 

            elif len(sizes) > 0:
                x=products.filter(sizes__id__in=sizes).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(sizes__id__in=sizes).order_by('-update_date').distinct()[:1] 

            elif  len(categorys) > 0:
                x=products.filter(category__id__in=categorys).order_by('-update_date').distinct().count()  
                count=x
                products=products.filter(category__id__in=categorys).order_by('-update_date').distinct()[:1] 

    else:
        count=products.filter(is_available=True).distinct().count()

        if storby :
            if storby == ['1']:
                products=products.filter(is_available=True).distinct()[:1]
            elif storby == ['2']:
                products=products.filter(is_available=True).order_by('product_name').distinct()[:1]
            elif storby == ['3']:
                products=products.filter(is_available=True).order_by('-product_name').distinct()[:1]
            elif storby == ['4']:#th reat
                products=products.filter(is_available=True).order_by('-product_name').distinct()[:1]
            elif storby == ['5']:
                products=products.filter(is_available=True).order_by('created_date').distinct()[:1]
            elif storby == ['6']:
                products=products.filter(is_available=True).order_by('price').distinct()[:1]
            elif storby == ['7']:
                products=products.filter(is_available=True).order_by('-price').distinct()[:1]
        else:
            products=products.filter(is_available=True).order_by('-update_date').distinct()[:1]




#=============================================
    if request.user.is_authenticated:
        is_fav=Favorite.objects.filter(user=request.user)
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    else:
        is_fav=Favorite.objects.filter(by_session=_favorit_id(request))
        id_products_list=[]
        for i in is_fav:
            get_id=i.product_id
            id_products_list.append(get_id)
    context={
        'products':products,
        'id_products_list':id_products_list,
    }
    template=render_to_string('ajax/products_filter.html',context)
    return JsonResponse({'data':template,'count':count})
