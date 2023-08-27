from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
    # get or creat cart
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    is_cart_item_exist=CartItem.objects.filter(product=product,cart=cart).exists()
    

    # check if request came from cart or product detail
    if 'cart' in request.META.get('HTTP_REFERER'):
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
        cart_item.save()

    # check if item herar 
    else:
        if is_cart_item_exist:
            cart_item=CartItem.objects.get(product=product,cart=cart)
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
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        # else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass


    
    # cart count
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user)
        # else:
        cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0

    data={'total':total,'grand_total':grand_total,'tax':tax,'cart_count':cart_count}
    return JsonResponse(data)






def DECREMENT_CART (request,total=0,quantity=0,cart_items=None):
    
    prod_id=request.GET.get('id')
    cart_item_id=request.GET.get('item_id')
    product=get_object_or_404(Product,id=prod_id)
    try:
        # if request.user.is_authenticated:
        #     cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        # else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    co=CartItem.objects.filter(cart=cart).count()
    
    try:
        tax=0
        grand_total=0
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        # else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass


    # cart count
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user)
        # else:
        cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0

    data={'total':total,'grand_total':grand_total,'tax':tax,'cart_count':cart_count}
    return JsonResponse(data)




def REMOVE_ITEM (request,total=0,quantity=0,cart_items=None):

    prod_id=request.GET.get('id')
    cart_item_id=request.GET.get('item_id')
    product=get_object_or_404(Product,id=prod_id)
    # if request.user.is_authenticated:
    #     cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    # else:
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()


    try:
        tax=0
        grand_total=0
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        # else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass

    data={'total':total,'grand_total':grand_total,'tax':tax}
    return JsonResponse(data)






def CART (request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        # if request.user.is_authenticated:
        #     cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        # else:
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
        'quantity':quantity,
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }
    return render (request,'cart/cart.html',context)