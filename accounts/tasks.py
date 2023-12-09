from celery import shared_task
import random
import string
from django.template.loader import render_to_string
from .models import Accounts
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from discounts.models import Discount_codes


@shared_task
def send_activation_code(uid,email,lang):
    
    user=Accounts._default_manager.get(pk=uid)
    numbers = string.digits 
    serial_list = [random.choice(numbers) for _ in range(6)]
    serial_string = ''.join(serial_list)
    if lang == 'en':

        mail_supject='Your account activation code'
        message=render_to_string('messeges/code_activation.html',{
            'email':email,
            'serial_string':serial_string,
        })
    else:
        mail_supject='رمز تفعيل حسابك'
        message=render_to_string('messeges/code_activation_ar.html',{
            'email':email,
            'serial_string':serial_string,
        })
    platn=strip_tags(message)
    to_email=email 
    from_email=settings.EMAIL_HOST_USER

    mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
    mess.attach_alternative(message,'text/html')
    mess.send()

    user.validation_code=serial_string
    user.sending_count-=1
    user.right_send= False
    user.save()
    return 'done'



@shared_task
def send_passwordreset_code(uid,email,lang):
    
    user=Accounts._default_manager.get(pk=uid)
    numbers = string.digits 
    serial_list = [random.choice(numbers) for _ in range(6)]
    serial_string = ''.join(serial_list)
    if lang == 'en':

        mail_supject='Password Reset'
        message=render_to_string('messeges/code_reset_pass.html',{
            'email':email,
            'serial_string':serial_string,
        })
    else:
        mail_supject='اعادة تعيين كلمة المرور'
        message=render_to_string('messeges/code_reset_pass_ar.html',{
            'email':email,
            'serial_string':serial_string,
        })


    platn=strip_tags(message)
    to_email=email 
    from_email=settings.EMAIL_HOST_USER

    mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
    mess.attach_alternative(message,'text/html')
    mess.send()
    user.validation_code=serial_string
    user.sending_count-=1
    user.right_send= False
    user.save()
    return 'done'



@shared_task
def send_welcome_msg(id):
    bouns_cod=Discount_codes.objects.create(discount=50)
    user=Accounts.objects.get(id=id)
    mail_supject='اهلا بك في جافا ستور'
    message=render_to_string('messeges/welcome_ar.html',{
        'user':user,
        'bouns_cod':bouns_cod,
    })
    platn=strip_tags(message)
    to_email=user.email 
    from_email=settings.EMAIL_HOST_USER
    mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
    mess.attach_alternative(message,'text/html')
    mess.send()
    return 'done'
