from .models import Product,Category
from django.db.models import Min,Max
from accounts.models import UserProfile

def LOOP_PRODUCT_CON (request):
    products=Product.objects.filter(is_available=True)
    minMaxPrice=products.aggregate(Min('price'),Max('price'))
    al_cats=Category.objects.all().distinct()
    if request.user.is_authenticated:
        count_fav=Product.objects.filter(favorits__email__iexact=request.user.email).count()
        userprofile=UserProfile.objects.get(user=request.user)
    else:
        count_fav=0
        userprofile=None
        
    data={
        'products':products,
        'minMaxPrice':minMaxPrice,
        'al_cats':al_cats,
        'count_fav':count_fav,
        'userprofile':userprofile,
    }

    return data




