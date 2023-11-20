from django.urls import path
from . import views


urlpatterns = [
    path('mk-order/',views.MK_ORDER,name='mk-order'),
    path('O-payment/',views.PAYMENT_PAGE,name='O-payment'),
    path('order_complete/',views.ORDER_COMPLEAT,name='order_complete'),
    path('check_order/',views.CHECK_ORDER,name='check_order'),
    path('gene-invo/<int:order_number>/',views.GENERATE_INVOICE,name='gene-invo'),
    path('payment-cancel/',views.payment_cancel,name='payment-cancel'),
    

]