from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.LOGIN,name='login'),
    path('login-function/',views.login_fuction,name='login-function'),

    path('singup/',views.SINGUP,name='singup'),
    path('singup_function/',views.singup_function,name='singup_function'),
    
    path('active/',views.activation_account,name='active'),

    path('input_emali_pass/',views.INPUT_EMAIL_PASS,name='input_emali_pass'),
    path('reset_password/',views.reset_passowrd,name='reset_password'),

    path('verif_code_activ/',views.verif_code_activ,name='verif_code_activ'),
    path('verification_code/',views.verification_code,name='verification_code'),

    path('new_password/',views.new_password,name='new_password'),


    path('logout/',views.LOG_OUT,name='logout'),

    path('resned_activ/',views.resend_msg_active,name='resned_activ'),
    path('resned_pass/',views.resend_msg_password,name='resned_pass'),


    path('on_popup/',views.on_popup,name='on_popup'),
    path('is_popup/',views.is_popup,name='is_popup'),
    path('profile/<int:id>/<str:slug>/',views.USER_PROFILE,name='profile'),
    path('edit_profile/<int:id>/<str:slug>/',views.EDIT_PROFILE,name='edit_profile'),
    path('change_password/<int:id>/<str:slug>/',views.CHANGE_PASSWORD,name='change_password'),
    path('your_orders/<int:num>/',views.YOUR_ORDERS,name='your_orders'),


]