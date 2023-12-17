from django.shortcuts import render
from .models import Product,ProductGallery,Category,Customizations,ReviewRating,Size_List,Color_List
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import secrets
from accounts.models import UserProfile
from django.views.generic.list import ListView
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
# Create your views here.

def PRODUCTS (request):
    if '/en/' in request.path:lang='en'
    else:lang='ar'
    if cache.get_many(['products','category','colors','sizes']):
        products=cache.get('products')
        category=cache.get('category')
        colors=cache.get('colors')
        sizes=cache.get('sizes')
    else:
        products=Product.objects.filter(is_available=True).order_by('?')[:8]
        category=Category.objects.all()
        sizes=Customizations.objects.filter(status=True).values('sizes__size_name','sizes__size_name_ar','sizes__id').distinct()
        colors=Customizations.objects.filter(status=True).values('colors__color_name','colors__color_code','colors__id').distinct()
        cache.set_many({'products':products,'sizes':sizes,'colors':colors,'category':category},5000)
    count_products=Product.objects.count()
    if request.user.is_authenticated:
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        all_favorit=[]
    

    context={
        'products':products,
        'category':category,
        'colors':colors,
        'sizes':sizes,
        'count_products':count_products,
        'lang':lang,
        'all_favorit':all_favorit,
    }
    return render(request,'store/products.html',context)



def QUICK_VIEW (request):
    id=request.GET.get('id')
    product=Product.objects.get(id=id)
    is_have_coustm=Customizations.objects.filter(product=product).exists()
    if '/en/' in request.path:
        lang='en'
        sizes=Customizations.objects.filter(status=True,product=product).values_list('sizes__size_name',flat=True).distinct()
        colors=Customizations.objects.filter(status=True,product=product).values_list('colors__color_name',flat=True).distinct()
    else:
        lang='ar'
        sizes=Customizations.objects.filter(status=True,product=product).values_list('sizes__size_name_ar',flat=True).distinct()
        colors=Customizations.objects.filter(status=True,product=product).values_list('colors__color_name_ar',flat=True).distinct()

    data={
        'colors':list (colors),
        'sizes':list (sizes),
        'lang':lang,
        'is_have_coustm':is_have_coustm,
    }
    return JsonResponse(data)

# @cache_page(2500)
def LOAD_MORE(request):
    colors=request.GET.getlist('_filterObj[color][]')
    sizes=request.GET.getlist('_filterObj[size][]')
    categorys=request.GET.getlist('_filterObj[category][]')
    offset=int(request.GET['offset'])#اللي موجود دلوقت ف الصفحه
    limit=int(request.GET['limit'])# اللي انا عينته عند الزرار 
    minPrice=request.GET.get('_filterObj[minPrice]')
    maxPrice=request.GET.get('_filterObj[maxPrice]')
    storby=request.GET.getlist('_filterObj[storby][]')
    search_kewrd=request.GET.get('search_kewrd')
    # creat random class
    # all_chars = string.ascii_letters + string.digits 
    # serial_list = [random.choice(all_chars) for _ in range(8)]
    # serial_string = ''.join(serial_list)
    random_1_fvort = secrets.token_hex(4).title().swapcase()
    random_2_qick = secrets.token_hex(4).title().swapcase()
    random_3_addmodal = secrets.token_hex(4).title().swapcase()
    random_4_select_size = secrets.token_hex(4).title().swapcase()
    random_5_color_cho = secrets.token_hex(4).title().swapcase()
    random_6_js_color = secrets.token_hex(4).title().swapcase()
    random_7_wrap_slik = secrets.token_hex(4).title().swapcase()

    #===================
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'



    if search_kewrd:
        if '/en/' in request.path:
            products=Product.objects.filter(Q(description__icontains=search_kewrd) | Q(product_name__icontains=search_kewrd)| Q(category__category_name__icontains=search_kewrd,is_available=True )).order_by('?')
        else:
            products=Product.objects.filter(Q(description_ar__icontains=search_kewrd) | Q(product_name_ar__icontains=search_kewrd)| Q(category__category_name_ar__icontains=search_kewrd,is_available=True )).order_by('?')
    else:
        products=Product.objects.filter(is_available=True).order_by('?').distinct()
        products=products.filter(price__gte=minPrice,price__lte=maxPrice)
    

    if colors or sizes or categorys:
        if len(colors) > 0 and len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct()[offset:offset+limit]


        elif  len(colors) > 0 and len(sizes) > 0 :
            x=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes).order_by('?').distinct()[offset:offset+limit]



        elif len(colors) > 0  and len(categorys) > 0 :
            x=products.filter(customizations__colors__id__in=colors,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,category__id__in=categorys).order_by('?').distinct()[offset:offset+limit]


        elif  len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct()[offset:offset+limit]

            
        else  :
            if len(colors) > 0:
                x=products.filter(customizations__colors__id__in=colors).order_by('?').distinct().count()  
                count=x
                products=products.filter(customizations__colors__id__in=colors).order_by('?').distinct()[offset:offset+limit]

            elif len(sizes) > 0:
                x=products.filter(customizations__sizes__id__in=sizes).order_by('?').distinct().count()  
                count=x
                products=products.filter(customizations__sizes__id__in=sizes).order_by('?').distinct()[offset:offset+limit]

            elif  len(categorys) > 0:
                x=products.filter(category__id__in=categorys).order_by('?').distinct().count()  
                count=x
                products=products.filter(category__id__in=categorys).order_by('?').distinct()[offset:offset+limit]

    else:
        count=products.filter(is_available=True).distinct().count()

        if storby :
            if storby == ['1']:
                products=products.filter(is_available=True).distinct()[offset:offset+limit]
            elif storby == ['2']:
                if '/en/' in request.path:
                    products=products.filter(is_available=True).order_by('product_name').distinct()[offset:offset+limit]
                else:
                    products=products.filter(is_available=True).order_by('product_name_ar').distinct()[offset:offset+limit]
            elif storby == ['3']:
                if '/en/' in request.path:
                    products=products.filter(is_available=True).order_by('-product_name').distinct()[offset:offset+limit]
                else:
                    products=products.filter(is_available=True).order_by('-product_name_ar').distinct()[offset:offset+limit]
            elif storby == ['4']:
                products=products.filter(is_available=True).order_by('-avg_rate').distinct()[offset:offset+limit]
            elif storby == ['5']:
                products=products.filter(is_available=True).order_by('?').distinct()[offset:offset+limit]
            elif storby == ['6']:
                products=products.filter(is_available=True).order_by('price').distinct()[offset:offset+limit]
            elif storby == ['7']:
                products=products.filter(is_available=True).order_by('-price').distinct()[offset:offset+limit]
        else:
            products=products.filter(is_available=True).order_by('?').distinct()[offset:offset+limit]

    if request.user.is_authenticated:
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        all_favorit=[]
    # if cache.get(f'products{offset}'):
    #     products=cache.get(f'products{offset}')
    #     for i in products:
    #         print(f'products{offset}')
    # else:
    #     print('from sql')
    #     cache.set(f'products{offset}',products,150)

#==============================================================

    context={
        'products':products,
        'random_1_fvort':random_1_fvort,
        'random_2_qick':random_2_qick,
        'random_3_addmodal':random_3_addmodal,
        'random_4_select_size':random_4_select_size,
        'random_5_color_cho':random_5_color_cho,
        'random_6_js_color':random_6_js_color,
        'random_7_wrap_slik':random_7_wrap_slik,
        'lang':lang,
        'all_favorit':all_favorit,
    }
    t=render_to_string('ajax/products_loadmore.html',context)
    return JsonResponse({'data':t,'count':count})




def PRODUCT_DETAILS (request,id):
    product=Product.objects.get(id=id)
    catigory=product.category
    products=Product.objects.filter(is_available=True,category=catigory).exclude(id=id).order_by('?')
    product_gallery=ProductGallery.objects.filter(product__id=product.id)

    sizes=Customizations.objects.filter(status=True,product=product).values('sizes__size_name','sizes__size_name_ar').distinct()
    colors=Customizations.objects.filter(status=True,product=product).values('colors__color_name','colors__color_name_ar').distinct()
    

    reviews=ReviewRating.objects.filter(status=True,product=product).order_by('-created_at')[:8]
    count_reviews=ReviewRating.objects.filter(status=True,product=product).order_by('-created_at').count()
    try:
        user=request.user
        profile_user=UserProfile.objects.get(user=user)
        valeue=ReviewRating.objects.get(product=product,user=profile_user).review
        rating=ReviewRating.objects.get(product=product,user=profile_user).rating
    except:
        valeue=None
        rating=None
    
    if request.user.is_authenticated:
        is_fav=product.favorits.filter(email__iexact=request.user.email).exists()
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        is_fav=False
        all_favorit=[]
    #==========
    
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
        

    context={
        'product':product,
        'product_gallery':product_gallery,
        'sizes':sizes,
        'colors':colors,
        'products':products,
        'reviews':reviews,
        'count_reviews':count_reviews,
        'valeue':valeue,
        'rating':rating,
        'lang':lang,
        'is_fav':is_fav,
        'all_favorit':all_favorit,
    }
    return render(request,'store/product_details.html',context)



def order_selection_filter(request):
    select_val=request.GET.get('select_val')
    prod_id=request.GET.get('id')
    #=========================
    if '/en/' in request.path:lang='en'
    else:lang='ar'
    #=================
    edit_action=[]
    is_have_coustm=Customizations.objects.filter(product__id=prod_id).exists()
    if select_val:
        if '/en/' in request.path:
            available_colors=Customizations.objects.filter(status=True,product__id=prod_id,sizes__size_name=select_val)
            for i in available_colors:
                edit_action.append(i.colors.color_name)
        else:
            available_colors=Customizations.objects.filter(status=True,product__id=prod_id,sizes__size_name_ar=select_val)
            for i in available_colors:
                edit_action.append(i.colors.color_name_ar)
        
    
    
    data={
        'edit_action':edit_action,
        'is_have_coustm':is_have_coustm,
        'lang':lang,
    }
    return JsonResponse(data)


def ADD_FAVORITE (request):
    if '/en/' in request.path:lang='en'
    else:lang='ar'

    id=request.GET.get('id')
    if request.user.is_authenticated:
        product=Product.objects.get(id=id)
        is_user_favorit=product.favorits.filter(email__iexact=request.user.email).exists()
        if is_user_favorit:
            product.favorits.remove(request.user)
        else:
            product.favorits.add(request.user)
        likes=product.favorits.count()
        count=Product.objects.filter(favorits__email__iexact=request.user.email).count()
        favorite=Product.objects.filter(favorits__email__iexact=request.user.email)
        
    else:
        likes=None
        count=0
    data={
        'likes':likes,
        'count':count,
        'lang':lang,
    }
    return JsonResponse(data)




class Favorite_Scroll(ListView):
    model=Product
    template_name='store/favorite.html'
    context_object_name='products'
    ordering='created_date'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(favorits__email__iexact=self.request.user.email,is_available=True).order_by('-favorits')[:8]
        return None
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context


def LOAD_FAVORITS(request):
    if '/en/' in request.path:lang='en'
    else:lang='ar'
    page=int( request.GET.get('page'))
    lent=int( request.GET.get('lent'))
    products=Product.objects.filter(favorits__email__iexact=request.user.email).order_by('-favorits')[lent:lent+page]
    count=Product.objects.filter(favorits__email__iexact=request.user.email).count()
    random_1_fvort = secrets.token_hex(4).title().swapcase()
    random_2_qick = secrets.token_hex(4).title().swapcase()
    random_3_addmodal = secrets.token_hex(4).title().swapcase()
    random_4_select_size = secrets.token_hex(4).title().swapcase()
    random_5_color_cho = secrets.token_hex(4).title().swapcase()
    random_6_js_color = secrets.token_hex(4).title().swapcase()
    random_7_wrap_slik = secrets.token_hex(4).title().swapcase()
    if request.user.is_authenticated:
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        all_favorit=[]
    context={
        'products':products,
        'random_1_fvort':random_1_fvort,
        'random_2_qick':random_2_qick,
        'random_3_addmodal':random_3_addmodal,
        'random_4_select_size':random_4_select_size,
        'random_5_color_cho':random_5_color_cho,
        'random_6_js_color':random_6_js_color,
        'random_7_wrap_slik':random_7_wrap_slik,
        'lang':lang,
        'all_favorit':all_favorit,
    }
    html=render_to_string('ajax/products_loadmore.html',context)
    data={'html':html,'count':count}
    return JsonResponse(data)






def SEARCH (request):
    if 'search' in request.GET:
        search=request.GET['search']
        if search:
            if '/en/' in request.path:
                products=Product.objects.filter(Q(description__icontains=search) | Q(product_name__icontains=search) | Q(category__category_name__icontains=search ) ).order_by('?')[:8]
            else:
                products=Product.objects.filter(Q(description_ar__icontains=search) | Q(product_name_ar__icontains=search ) | Q(category__category_name_ar__icontains=search ) ).order_by('?')[:8]
            count_products=Product.objects.count()
    context={
        'products':products,
        'count_products':count_products,
    }
    return render (request,'store/search.html',context)


# @cache_page(2500)
def FILTER(request):
    colors=request.GET.getlist('_filterObj[color][]')
    sizes=request.GET.getlist('_filterObj[size][]')
    categorys=request.GET.getlist('_filterObj[category][]')
    minPrice=request.GET.get('_filterObj[minPrice]')
    maxPrice=request.GET.get('_filterObj[maxPrice]')
    storby=request.GET.getlist('_filterObj[storby][]')
    search_kewrd=request.GET.get('search_kewrd')
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'

    if search_kewrd:
        if '/en/' in request.path:
            products=Product.objects.filter(Q(description__icontains=search_kewrd) | Q(product_name__icontains=search_kewrd)| Q(category__category_name__icontains=search_kewrd,is_available=True )).order_by('?')
        else:
            products=Product.objects.filter(Q(description_ar__icontains=search_kewrd) | Q(product_name_ar__icontains=search_kewrd)| Q(category__category_name_ar__icontains=search_kewrd,is_available=True )).order_by('?') 
    else:
        products=Product.objects.filter(is_available=True).order_by('?').distinct()
        products=products.filter(price__gte=minPrice,price__lte=maxPrice)
        


    if colors or sizes or categorys:
        if len(colors) > 0 and len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct()[:8]


        elif  len(colors) > 0 and len(sizes) > 0 :
            x=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,customizations__sizes__id__in=sizes).order_by('?').distinct()[:8]



        elif len(colors) > 0  and len(categorys) > 0 :
            x=products.filter(customizations__colors__id__in=colors,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__colors__id__in=colors,category__id__in=categorys).order_by('?').distinct()[:8]


        elif  len(sizes) > 0 and len(categorys) > 0 :
            x=products.filter(customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct().count()  
            count=x
            products=products.filter(customizations__sizes__id__in=sizes,category__id__in=categorys).order_by('?').distinct()[:8]

            
        else  :
            if len(colors) > 0:
                x=products.filter(customizations__colors__id__in=colors).order_by('?').distinct().count()  
                count=x
                products=products.filter(customizations__colors__id__in=colors).order_by('?').distinct()[:8] 

            elif len(sizes) > 0:
                x=products.filter(customizations__sizes__id__in=sizes).order_by('?').distinct().count()  
                count=x
                products=products.filter(customizations__sizes__id__in=sizes).order_by('?').distinct()[:8] 

            elif  len(categorys) > 0:
                x=products.filter(category__id__in=categorys).order_by('?').distinct().count()  
                count=x
                products=products.filter(category__id__in=categorys).order_by('?').distinct()[:8] 

    else:
        count=products.filter(is_available=True).distinct().count()

        if storby :
            if storby == ['1']:
                products=products.filter(is_available=True).distinct()[:8]
            elif storby == ['2']:
                if '/en/' in request.path:
                    products=products.filter(is_available=True).order_by('product_name').distinct()[:8]
                else:
                    products=products.filter(is_available=True).order_by('product_name_ar').distinct()[:8]
            elif storby == ['3']:
                if '/en/' in request.path:
                    products=products.filter(is_available=True).order_by('-product_name').distinct()[:8]
                else:
                    products=products.filter(is_available=True).order_by('-product_name_ar').distinct()[:8]
            elif storby == ['4']:
                products=products.filter(is_available=True).order_by('-avg_rate').distinct()[:8]
            elif storby == ['5']:
                products=products.filter(is_available=True).order_by('?').distinct()[:8]
            elif storby == ['6']:
                products=products.filter(is_available=True).order_by('price').distinct()[:8]
            elif storby == ['7']:
                products=products.filter(is_available=True).order_by('-price').distinct()[:8]
        else:
            products=products.filter(is_available=True).order_by('?').distinct()[:8]

    if request.user.is_authenticated:
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        all_favorit=[]
#=============================================
    

    context={
        'products':products,
        'lang':lang,
        'all_favorit':all_favorit,
    }
    template=render_to_string('ajax/products_filter.html',context)
    return JsonResponse({'data':template,'count':count})


def SAVE_REVIEW (request,id):
    if '/en/' in request.path:lang='en'
    else:lang='ar'
    button=request.POST.get('button')
    direction=(request.POST.get('direction'))
    product=Product.objects.get(id=id)
    user=request.user
    user_profile=UserProfile.objects.get(user=user)
    if button == 'post':
        review=ReviewRating.objects.create(
            product=product,
            user=user_profile,
            review=request.POST.get('info[1][review]'),
            rating=request.POST.get('info[2][rating]'),
            ip=request.META.get('REMOTE_ADDR'),
            )
        product.avg_rate=product.averegeReview()
        product.save()
    elif button == 'edit':
        edit_review=ReviewRating.objects.get(product=product,user=user_profile)
        if request.POST.get('info[1][review]') != edit_review.review:
            edit_review.review=request.POST.get('info[1][review]')
            edit_review.direction = direction
        edit_review.rating=request.POST.get('info[2][rating]')
        edit_review.save()
        product.avg_rate=product.averegeReview()
        product.save()
    elif button == 'delete':
        edit_review=ReviewRating.objects.get(product=product,user=user_profile).delete()
        product.avg_rate=product.averegeReview()
        product.save()

    reviews=ReviewRating.objects.filter(status=True,product=product).order_by('-created_at')[:8]
    count=ReviewRating.objects.filter(status=True,product=product).order_by('-created_at').count()
    template_rev=render_to_string('ajax/reviews.html',{'reviews':reviews})
    is_rev_exi=ReviewRating.objects.filter(user=user_profile,product=product).exists()
    data={
        'bool':True,
        'template_rev':template_rev,
        'count':count,
        'is_rev_exi':is_rev_exi,
        'lang':lang,
        }
    return JsonResponse(data)


def LOAD_REVIEW(request):
    id=request.GET.get('id')
    reviw_showed=int (request.GET.get('reviw_showed'))
    limit= int (request.GET.get('limit'))
    reviews=ReviewRating.objects.filter(status=True,product__id=id).order_by('-created_at')[reviw_showed:reviw_showed+limit]
    template=render_to_string('ajax/reviews_load.html',{'reviews':reviews})
    data={'template':template}
    return JsonResponse(data)






def check_lang(request):
    url=None
    if '/en/' in request.path:
        if '/en/' in request.path and '/en/' not in  request.META.get('HTTP_REFERER'):
            url=request.META.get('HTTP_REFERER').replace("/ar/", "/")
    elif '/ar/' in request.path:
        if '/ar/' in request.path and '/ar/' not in  request.META.get('HTTP_REFERER'):
            url=request.META.get('HTTP_REFERER').replace("/en/", "/")
    data={'url':url}
    return JsonResponse(data)



@receiver(post_save,sender=Product)
def clear_cache_post_save(*args,**kwargs):
    cache.clear()
@receiver(post_delete,sender=Product)
def clear_cache_post_delete(*args,**kwargs):
    cache.clear()










