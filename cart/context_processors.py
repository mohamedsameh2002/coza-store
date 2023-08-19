from .models import *
from .views import _cart_id
from django.shortcuts import render
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def COUNTER_ITEM_CON (request):
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
    return dict (cart_count=cart_count)


def CART_CON (request,total=0,quantity=0,cart_items=None):
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

    return dict (cart_items=cart_items,total=total)
