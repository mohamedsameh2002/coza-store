from .models import Product,Favorite,Category,Favorite_storeg_id
from django.db.models import Min,Max
from .views import _favorit_id
def LOOP_PRODUCT_CON (request):
    products=Product.objects.filter(is_available=True)
    minMaxPrice=products.aggregate(Min('price'),Max('price'))
    if request.user.is_authenticated:
        count_fav=Favorite.objects.filter(user=request.user).count()
    else:
        try:
            fave_storeg=Favorite_storeg_id.objects.get(favorite_id=_favorit_id(request))
        except Favorite_storeg_id.DoesNotExist:
            fave_storeg=Favorite_storeg_id.objects.create(favorite_id=_favorit_id(request))
        fave_storeg.save()
        count_fav=Favorite.objects.filter(by_session=fave_storeg).count()
    al_cats=Category.objects.all().distinct()
        
    data={
        'products':products,
        'count_fav':count_fav,
        'minMaxPrice':minMaxPrice,
        'al_cats':al_cats,
    }

    return data

