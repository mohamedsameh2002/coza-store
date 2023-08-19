from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('',views.CART,name='cart'),
    path('add_cart/<uuid:prod_id>/',views.ADD_CART,name='add_cart'),
    path('decrement_cart/<uuid:prod_id>/<int:cart_item_id>/',views.DECREMENT_CART,name='decrement_cart'),
    path('remove_item/<uuid:prod_id>/<int:cart_item_id>/',views.REMOVE_ITEM,name='remove_item'),
    # path('chekout/',views.chekout,name='chekout'),

]

