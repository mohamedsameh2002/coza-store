from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('',views.CART,name='cart'),
    path('add_cart/',views.ADD_CART,name='add_cart'),
    path('decrement_cart/',views.DECREMENT_CART,name='decrement_cart'),
    path('remove_item/',views.REMOVE_ITEM,name='remove_item'),
    path('chekout/',views.CHEKOUT,name='chekout'),

]
