from django.urls import path
from . import views
from django.conf import settings
from . import context_processors
urlpatterns = [
    path('',views.PRODUCTS,name='store'),
    path('<uuid:id>/',views.PRODUCT_DETAILS,name='product_details'),
    path('add_favorite/',views.ADD_FAVORITE,name='add_favorite'),
    path('favorite/',views.FAVORITE_PAGE,name='favorite'),
    path('load/',views.LOAD_MORE,name='load'),

]