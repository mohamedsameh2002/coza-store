from celery import shared_task
from django.template.loader import render_to_string
from .models import Order,OrderProduct
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from accounts.models import Accounts


@shared_task
def order_completion_message(id,order_number,lang):
    user=Accounts._default_manager.get(id=id)
    order=Order.objects.get(user=user,order_numper=order_number,is_order=True)
    order_products=OrderProduct.objects.filter(order__id=order.id)
    if lang =='en':
        mail_supject='Your order has been completed'
        message=render_to_string('messeges/order_completed.html',{
            'user':user,
            'order':order,
            'order_products':order_products,
            'lang':lang,
        })
    else:
        lang='ar'
        mail_supject='تم اكتمال طلبك'
        message=render_to_string('messeges/order_completed_ar.html',{
            'user':user,
            'order':order,
            'order_products':order_products,
            'lang':lang,
            })
    platn=strip_tags(message)
    to_email=order.email 
    from_email=settings.EMAIL_HOST_USER
    mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
    mess.attach_alternative(message,'text/html')
    mess.send()
    order.order_E_mesg = True
    order.save()
    return 'done'

