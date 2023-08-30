from django.urls import path
from . import views


urlpatterns = [
    path('pyment',views.GO_PYMENT,name='go_pyment'),
    path('paymentes/',views.PAYMENTES,name='paymentes'),
    path('order_complete/',views.ORDER_COMPLEAT,name='order_complete'),
    

]