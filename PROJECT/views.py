from django.shortcuts import render
from store.models import Product
from django.contrib.auth.decorators import login_required



def home (request):
    products=Product.objects.filter(is_available=True).order_by('-update_date')
    all_favorit=[]
    if request.user.is_authenticated:
        all_favorit=list(Product.objects.filter(favorits__email__iexact=request.user.email))
    else:
        all_favorit=[]
    context={
        'products':products,
        'all_favorit':all_favorit,
    }
    return render(request,'home.html',context)


def ABOUT (request):
    return render(request,'project/about.html',)

@login_required
def HELP (request):
    help_rq=request.GET.get('help')
    return render(request,'project/help.html',{'help_rq':help_rq})


def error_404_page(request,exception):
    return render(request,'project/error_page.html')