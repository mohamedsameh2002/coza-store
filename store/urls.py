from django.urls import path
from . import views

urlpatterns = [
    path('',views.PRODUCTS,name='store'),
    path('<uuid:id>/',views.PRODUCT_DETAILS,name='product_details'),
    path('order_selection_filter/',views.order_selection_filter,name='order_selection_filter'),
    path('add_favorite/',views.ADD_FAVORITE,name='add_favorite'),
    path('favorite/',views.Favorite_Scroll.as_view(),name='favorite'),
    path('quick/',views.QUICK_VIEW,name='quick'),
    path('search/',views.SEARCH,name='search'),
    path('filter-data/',views.FILTER,name='filter_data'),
    path('load/',views.LOAD_MORE,name='load'),
    path('satve-review/<uuid:id>/',views.SAVE_REVIEW,name='satve-review'),
    path('load_review/',views.LOAD_REVIEW,name='satve-review'),
    path('check_lang/',views.check_lang,name='check_lang'),
    path('load_faveorits/',views.LOAD_FAVORITS,name='load_faveorits'),

]