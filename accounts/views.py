import random
import string
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages,auth
from cart.models import Cart,CartItem,Temporary_cart
from cart.views import _cart_id
from store.models import Product,Favorite,Favorite_storeg_id
from store.views import _favorit_id
from accounts.models import Accounts,UserProfile
from .forms import SingupForm,UserprofileForm
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives


def SINGUP (request):
    if request.method == 'POST':
        form=SingupForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.is_active=False
            user.right_send=True
            user.save()
            pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
            tivk=default_token_generator.make_token(user)
            return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
        else:
            email=request.POST.get('email')
            is_exist=Accounts.objects.filter(email__exact=email).exists()
            if is_exist:
                user=Accounts.objects.get(email__exact=email)
                if user.is_active == False:
                    pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
                    tivk=default_token_generator.make_token(user)
                    return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
                else:
                    pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
                    tivk=default_token_generator.make_token(user)
                    return redirect('/accounts/login/?command=redilog&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
    return render(request,'registration/singup.html')

def activation_account (request):
    email=request.GET.get('email')
    pibszzzz=request.GET.get('pibszzzz')
    tivk=request.GET.get('tivk')
#=========
    uid=urlsafe_base64_decode(pibszzzz).decode()
    user=Accounts._default_manager.get(pk=uid)
    if user.is_active==True:
        return redirect ('home')
    else:
        if user is not None and default_token_generator.check_token(user,tivk) and user.right_send == True and user.sending_count > 0:
            numbers = string.digits 
            serial_list = [random.choice(numbers) for _ in range(6)]
            serial_string = ''.join(serial_list)
            mail_supject='code activation'
            message=render_to_string('messeges/code_activation.html',{
                'user':user,
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
            
        else:
            print('nooooooooo')

        if request.method == 'POST':
            input_msg=request.POST.get('code_acti')
            if input_msg == user.validation_code:
                user.is_active =True
                user.right_send= True
                user.sending_count=5
                user.save()
                profile=UserProfile.objects.create(user=user)
                profile.save
                print('yeees')
                messages.success(request,'the email is acctiave success')
                return redirect('login')
            else:
                print('not activation')
        
        return render(request,'registration/input_numbers.html')



def LOGIN (request):
    email_value=None
    if 'redilog' in request.GET.get('command', ''):
        messages.info(request,'the email oredy cryated')
        email=request.GET.get('email')
        email_value=email
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_items=CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        product=Product.objects.get(id=item.product.id)
                        color=item.color
                        size=item.size
                        isex=CartItem.objects.filter(product=product,user=user,color=color,size=size).exists()
                        if isex:
                            user_p=CartItem.objects.get(product=product,user=user,color=color,size=size)
                            user_p.quantity+=item.quantity
                            user_p.save()
                            item.delete()
                            
                        else:
                            item.user=user
                            item.cart=None
                            item.save()
                    cart.delete()
            except:
                pass
            try:
                fave_storeg=Favorite_storeg_id.objects.get(favorite_id=_favorit_id(request))
                is_favorit_exist=Favorite.objects.filter(by_session=fave_storeg).exists()
                if is_favorit_exist:
                    favorits=Favorite.objects.filter(by_session=fave_storeg)
                    for fav in favorits:
                        fav_product=Product.objects.get(id=fav.product.id)
                        isfav_ex_inuser=Favorite.objects.filter(user=user,product=fav_product).exists()
                        if isfav_ex_inuser :
                            x=Favorite.objects.get(by_session=fave_storeg,product=fav_product)
                            x.delete()
                        else:
                            fav.user=user
                            fav.by_session=None
                            fav.save()
                    fave_storeg.delete()
            except:
                pass
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invaled login ')
            return redirect('login')
        
    return render(request,'registration/login.html',{'email_value':email_value})


def login_fuction(request):
    email=request.GET.get('email')
    is_exist=Accounts.objects.filter(email=email).exists()

    data={
        'is_exist':is_exist,
    }
    return JsonResponse(data)


def INPUT_EMAIL_PASS (request):
    if request.method == 'POST':
        try:
            email=request.POST.get('email_reset')
            user=Accounts.objects.get(email__exact=email)
            fseq=urlsafe_base64_encode(force_bytes(user.pk))
            aw=default_token_generator.make_token(user)
            return redirect('/accounts/reset_password/?command=reset_pass&email='+email+'&fseq='+fseq+'&aw='+aw)
        except:
            messages.warning(request,'pless chek for the email')
            return redirect('input_emali_pass')
    return render(request,'registration/reset_pass_email.html')

def reset_passowrd(request):
    email=request.GET.get('email')
    fseq=request.GET.get('fseq')
    aw=request.GET.get('aw')
    uid=urlsafe_base64_decode(fseq).decode()
    user=Accounts._default_manager.get(pk=uid)
#=========
    if user.is_active==False:
        messages.error(request,'your account is not activate yet , يعرص')
        return redirect ('login')
    else:
        if user is not None and default_token_generator.check_token(user,aw) and user.right_send == True and user.sending_count > 0:
            numbers = string.digits 
            serial_list = [random.choice(numbers) for _ in range(6)]
            serial_string = ''.join(serial_list)
            if '/en/' in request.path:
                mail_supject='Password Reset'
                message=render_to_string('messeges/code_reset_pass.html',{
                    'user':user,
                    'email':email,
                    'serial_string':serial_string,
                })
            else:
                mail_supject='اعادة تعيين كلمة المرور'
                message=render_to_string('messeges/code_reset_pass_ar.html',{
                    'user':user,
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
            request.session['uid']=uid
        else:
            print('nooooooooo')

        if request.method == 'POST':
            input_msg=request.POST.get('code_reset')
            if input_msg == user.validation_code:
                user.right_send= True
                user.sending_count=5
                user.save()
                messages.success(request,'validate is corrita')
                return redirect('new_password')
            else:
                print('not reseted')
    return render(request,'registration/inbut_num_pass.html')


def new_password (request):
    if request.method == 'POST':
        password=request.POST['password']
        conf_password=request.POST['conf_password']
        if password == conf_password:
            if len(password) < 6:
                messages.error(request,'Please enter a password containing at least 6 elements')
                return redirect('new_password')
            else :
                uid=request.session.get('uid')
                user=Accounts.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'password reseted succsessful')
                return redirect('login')
        else:
            messages.warning(request,'password dont match')
            return redirect('new_password')
    else:
        return render(request,'registration/new_password.html')

@login_required(login_url='login')
def LOG_OUT (request):
    auth.logout(request)
    messages.info(request,'log out')
    return redirect('login')



def resend_msg_active(request):
    email=request.GET.get('email')
    pibszzzz=request.GET.get('pibszzzz')
    tivk=request.GET.get('tivk')

#=========
    uid=urlsafe_base64_decode(pibszzzz).decode()
    user=Accounts._default_manager.get(pk=uid)
    if user.is_active==True:
        return redirect ('home')
    else:
        if user is not None and default_token_generator.check_token(user,tivk)  and user.sending_count > 0:
            numbers = string.digits 
            serial_list = [random.choice(numbers) for _ in range(6)]
            serial_string = ''.join(serial_list)
            mail_supject='code activation'
            message=render_to_string('messeges/code_activation.html',{
                'user':user,
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
        else:
            print('nooooooooo')

    data={

    }
    return JsonResponse(data)

def resend_msg_password(request):
    email=request.GET.get('email')
    fseq=request.GET.get('fseq')
    aw=request.GET.get('aw')
    uid=urlsafe_base64_decode(fseq).decode()
    user=Accounts._default_manager.get(pk=uid)
#=========
    if user.is_active==False:
        messages.error(request,'your account is not activate yet , يعرص')
        return redirect ('login')
    else:
        if user is not None and default_token_generator.check_token(user,aw)  and user.sending_count > 0:
            numbers = string.digits 
            serial_list = [random.choice(numbers) for _ in range(6)]
            serial_string = ''.join(serial_list)
            mail_supject='code reset password'
            message=render_to_string('messeges/code_reset_pass.html',{
                'user':user,
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
        else:
            print('nooooooooo')

    data={

    }
    return JsonResponse(data)


def make_tep_session (request):
    session_key=request.session.session_key
    tep=Temporary_cart.objects.create(temporary_id=session_key)
    tep.save()
    
    data={
        
    }
    return JsonResponse(data)