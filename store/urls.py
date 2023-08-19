from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('',views.PRODUCTS,name='store'),
    path('<uuid:id>/',views.PRODUCT_DETAILS,name='product_details'),
    path('add_favorite/<uuid:prod_id>/',views.ADD_FAVORITE,name='add_favorite'),
    path('favorite/',views.FAVORITE_PAGE,name='favorite'),

]

