from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('login/',views.LOGIN,name='login'),
    path('login-function/',views.login_fuction,name='login-function'),

    path('singup/',views.SINGUP,name='singup'),
    path('active/',views.activation_account,name='active'),

]