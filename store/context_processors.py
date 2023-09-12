from .models import Product,Favorite
from django.db.models import Min,Max
from .views import _favorit_id
def LOOP_PRODUCT_CON (request):
    products=Product.objects.filter(is_available=True)
    minMaxPrice=products.aggregate(Min('price'),Max('price'))
    if request.user.is_authenticated:
        count_fav=Favorite.objects.filter(user=request.user).count()
    else:
        count_fav=Favorite.objects.filter(by_session=_favorit_id(request)).count()
        
    data={
        'products':products,
        'count_fav':count_fav,
        'minMaxPrice':minMaxPrice,
    }

    return data

