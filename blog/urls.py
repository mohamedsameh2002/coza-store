from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('',views.BLOG,name='blog'),
    path('<str:slug>/<int:id>/',views.BLOG_DETAIL,name='blog_detail'),
    path('search-blog/',views.SEARCH,name='search-blog'),
    path('identifiers/',views.OTHER_IDENTIFIERS,name='identifiers'),

]