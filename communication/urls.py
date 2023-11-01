from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('chat/',views.CHAT_PAGE,name='chat'),
    path('about/',views.ABOUT,name='about'),
    
]