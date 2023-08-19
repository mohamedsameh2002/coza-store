from .models import Product,Favorite

def LOOP_PRODUCT_CON (request):
    products=Product.objects.all()
    count_fav=Favorite.objects.filter(user=request.user).count()# becarful error if you loged out
    return dict(products=products,count_fav=count_fav)