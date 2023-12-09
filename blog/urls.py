from django.urls import path
from . import views
urlpatterns = [
    path('',views.BLOG,name='blog'),
    path('tag/<slug:tag_slug>/',views.BLOG,name='blog_bytag'),
    path('<str:slug>/<int:id>/',views.BLOG_DETAIL,name='blog_detail'),
    path('search-blog/',views.SEARCH,name='search-blog'),
    path('identifiers/',views.OTHER_IDENTIFIERS,name='identifiers'),
    path('add_comment/',views.ADD_COMMENT,name='add_comment'),
    path('add_reply/',views.ADD_REPLY,name='add_reply'),
    path('delet_com_rep/<int:id>/<str:val>/',views.DELET_COM_Rep,name='delet_com_rep'),
    path('load_comments/',views.LOAD_COMMENTS,name='load_comments'),
    path('hide_noti_icon/',views.hide_noti_icon,name='hide_noti_icon'),

]