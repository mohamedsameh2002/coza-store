from .models import Product,Category
from django.db.models import Min,Max

def LOOP_PRODUCT_CON (request):
    products=Product.objects.filter(is_available=True)
    minMaxPrice=products.aggregate(Min('price'),Max('price'))
    al_cats=Category.objects.all().distinct()
    count_fav=Product.objects.filter(favorits__email__iexact=request.user.email).count()
        
    data={
        'products':products,
        'minMaxPrice':minMaxPrice,
        'al_cats':al_cats,
        'count_fav':count_fav,
    }

    return data

