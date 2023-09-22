from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from discounts.models import Discount_codes
from accounts.models import UserProfile

# Create your views here.
def _cart_id (request):
    cart=request.session.session_key
    if not cart :
        cart=request.session.create()
    return cart


def ADD_CART (request,total=0,quantity=0,cart_items=None):
    # glopel variaple

    prod_id=request.GET.get('id')
    sizes=request.GET.get('size')
    colors=request.GET.get('color')
    qty=request.GET.get('qty')
    url=request.META.get('HTTP_REFERER')
    user=request.user
    product=Product.objects.get(id=prod_id)
    #=========================================

    if request.user.is_authenticated:
        is_cart_item_exist=CartItem.objects.filter(product=product,user=user,color=colors,size=sizes).exists()
        # check if request came from cart or product detail
        if 'cart' in request.META.get('HTTP_REFERER'):
            color=request.GET.get('color')
            size=request.GET.get('size')
            cart_item=CartItem.objects.get(product=product,user=user,color=color,size=size)
            cart_item.quantity+=1
            cart_item.save()
            
        # check if item herar 
        else:
            if is_cart_item_exist :
                cart_item=CartItem.objects.get(product=product,user=user,color=colors,size=sizes)
                cart_item.quantity+=int(qty)
                cart_item.save()
            else:
                cart_item=CartItem.objects.create(
                    product=product,
                    quantity=qty,
                    user=user,
                    size=sizes,
                    color=colors,
                    )
            
    else:
        # get or creat cart
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exist=CartItem.objects.filter(product=product,cart=cart,color=colors,size=sizes).exists()

        # check if request came from cart or product detail
        if 'cart' in request.META.get('HTTP_REFERER'):
            cart_item=CartItem.objects.get(product=product,cart=cart,color=colors,size=sizes)
            cart_item.quantity+=1
            cart_item.save()

        # check if item herar 
        else:
            if is_cart_item_exist :
                cart_item=CartItem.objects.get(product=product,cart=cart,color=colors,size=sizes)
                cart_item.quantity+=int(qty)
                cart_item.save()
            else:
                cart_item=CartItem.objects.create(
                    product=product,
                    quantity=qty,
                    cart=cart,
                    size=sizes,
                    color=colors,
                    )
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
            
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass

    total_discount=0
    if request.user.is_authenticated:
        user_profile=UserProfile.objects.get(user=user)
        if user_profile.discount_cods.exists():
            # codes=user_profile.discount_cods.all()
            codes=user_profile.discount_cods.values_list('code',flat=True)
            for code in codes:
                discount=Discount_codes.objects.get(code=code).discount
                total_discount+=discount
            if total < total_discount:
                total=0
                grand_total=tax
            else :
                total = total - total_discount
                grand_total=total+tax
    
    # cart count
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0
    #========
    if request.user.is_authenticated:
        cart_items=CartItem.objects.filter(user=request.user,in_active=True)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
    templ_side_cart=render_to_string('ajax/sid_cart.html',{'cart_items':cart_items})
    #==========
    
    data={'total':total,'grand_total':grand_total,'tax':tax,'cart_count':cart_count,'templ_side_cart':templ_side_cart}
    return JsonResponse(data)






def DECREMENT_CART (request,total=0,cart_items=None):
    color=request.GET.get('color')
    size=request.GET.get('size')
    prod_id=request.GET.get('id')

    product=get_object_or_404(Product,id=prod_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,color=color,size=size)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,color=color,size=size)

        if cart_item.quantity > 1 :
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
            
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass

    total_discount=0
    if request.user.is_authenticated:
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        if user_profile.discount_cods.exists():
            # codes=user_profile.discount_cods.all()
            codes=user_profile.discount_cods.values_list('code',flat=True)
            for code in codes:
                discount=Discount_codes.objects.get(code=code).discount
                total_discount+=discount
            if total < total_discount:
                total=0
                grand_total=tax
            else :
                total = total - total_discount
                grand_total=total+tax


    # cart count
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0
    
    #========
    if request.user.is_authenticated:
        cart_items=CartItem.objects.filter(user=request.user,in_active=True)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
    template=render_to_string('ajax/cart_aj.html',{'cart_items':cart_items})
    template_2=render_to_string('ajax/cart_emty_aj.html')
    templ_side_cart=render_to_string('ajax/sid_cart.html',{'cart_items':cart_items})
#========
    data={'total':total,'grand_total':grand_total,'tax':tax,'cart_count':cart_count,'template':template,'template_2':template_2,'templ_side_cart':templ_side_cart}
    return JsonResponse(data)




def REMOVE_ITEM (request,total=0,cart_items=None):
    color=request.GET.get('color')
    size=request.GET.get('size')
    prod_id=request.GET.get('id')
    product=get_object_or_404(Product,id=prod_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,color=color,size=size)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,color=color,size=size)
    cart_item.delete()


    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
            
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass


    total_discount=0
    if request.user.is_authenticated:
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        if user_profile.discount_cods.exists():
            # codes=user_profile.discount_cods.all()
            codes=user_profile.discount_cods.values_list('code',flat=True)
            for code in codes:
                discount=Discount_codes.objects.get(code=code).discount
                total_discount+=discount
            if total < total_discount:
                total=0
                grand_total=tax
            else :
                total = total - total_discount
                grand_total=total+tax

    # cart count
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0
    

#========
    if request.user.is_authenticated:
        cart_items=CartItem.objects.filter(user=request.user,in_active=True)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        
    template=render_to_string('ajax/cart_aj.html',{'cart_items':cart_items})
    template_2=render_to_string('ajax/cart_emty_aj.html')
    templ_side_cart=render_to_string('ajax/sid_cart.html',{'cart_items':cart_items})

#========
    data={'total':total,'grand_total':grand_total,'tax':tax,'cart_count':cart_count,'template':template,'template_2':template_2,'templ_side_cart':templ_side_cart}
    return JsonResponse(data)






def CART (request,total=0,quantity=0,cart_items=None):

    if request.method == 'POST':
        code=request.POST.get('coupon')
        try:
            user=request.user
            user_profile=UserProfile.objects.get(user=user)
            discount_code=Discount_codes.objects.get(code=code)
            code_valeu=discount_code.discount
            if discount_code.active == True :
                user_profile.discount_cods.add(discount_code)
                discount_code.active=False
                discount_code.save()
                messages.success(request,f'You are now using a discount code worth $ {code_valeu},The code will expire upon completion of payment')
            else:
                messages.warning(request,'You entered the wrong code or it may have expired')
        except:
            if request.user.is_authenticated:
                messages.warning(request,'You entered the wrong code or it may have expired')
            else:
                messages.warning(request,'Please log in first to use the discount code')
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
            
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass


    total_discount=0
    if request.user.is_authenticated:
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        if user_profile.discount_cods.exists():
            # codes=user_profile.discount_cods.all()
            codes=user_profile.discount_cods.values_list('code',flat=True)
            for code in codes:
                discount=Discount_codes.objects.get(code=code).discount
                total_discount+=discount
            if total < total_discount:
                total=0
                grand_total=tax
            else :
                total = total - total_discount
                grand_total=total+tax
    
        
        
    context={
        'quantity':quantity,
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'total_discount':total_discount,
        
        }
    return render (request,'cart/cart.html',context)



@login_required(login_url="login")
def CHEKOUT (request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass
    context={
        'total':total,
        'quantity':quantity,
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }

    return render (request,'cart/chekout.html',context)
