from django.shortcuts import render,redirect
from store.models import Product



def home (request):
    products=Product.objects.filter(is_available=True).order_by('-update_date')

    context={
        'products':products,
    }
    return render(request,'home.html',context)