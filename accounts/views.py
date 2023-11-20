import random
import string
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages,auth
from cart.models import Cart,CartItem
from cart.views import _cart_id
from store.models import Product
from accounts.models import Accounts,UserProfile
from .forms import SingupForm
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
            # x=form.save(commit=False)
            # x.is_active=False
            # x.save()
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.is_active=False
            user.right_send=True
            user.is_manual=True
            user.save()
            pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
            tivk=default_token_generator.make_token(user)
            return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
        else:
            email=request.POST.get('email')
            is_exist=Accounts.objects.filter(email__iexact=email).exists()
            if is_exist:
                user=Accounts.objects.get(email__iexact=email)
                if user.is_active == False:
                    pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
                    tivk=default_token_generator.make_token(user)
                    return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
                else:
                    pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
                    tivk=default_token_generator.make_token(user)
                    return redirect('/accounts/login/?command=redilog&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
            else:
                if '/en/' in request.path:
                    messages.error(request,'There is an error, please check your data')
                else:
                    messages.error(request,'هناك خطأ ، يرجي التحقق من بياناتك')
    return render(request,'registration/singup.html')


def singup_function (request):
    is_exist=True
    email=request.GET.get('email')
    password=request.GET.get('password')
    if '@' in str (email) and '.' in str (email) and any(str(char).isalpha() for char in str (email)):
        if str (email).index('@') > 0 and len(str (email)) > str (email).index('@') + 1:
            is_exist=False
    else:
        is_exist=True

    is_good=False
    if password:
        if len(password) >= 6 :
            is_good=True
    data={
        "is_exist":is_exist,
        "is_good":is_good,
    }
    return JsonResponse (data)


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
            # mess.send()

            user.validation_code=serial_string
            user.sending_count-=1
            user.right_send= False
            user.save()
            
        else:
            pass
        sendeng_cocunt=user.sending_count
        return render(request,'registration/input_numbers.html',{'sendeng_cocunt':sendeng_cocunt,'email':email})



def verif_code_activ (request):
    verification=None
    pibszzzz=request.GET.get('pibszzzz')
    uid=urlsafe_base64_decode(pibszzzz).decode()
    user=Accounts._default_manager.get(pk=uid)
    sendeng_cocunt=user.sending_count
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
    theCode=request.GET.get('theCode')
    if theCode == user.validation_code:
        user.is_active =True
        user.right_send= True
        user.sending_count=5
        user.validation_code=None
        user.save()
        profile=UserProfile.objects.create(user=user)
        profile.save
        if '/en/' in request.path:
            messages.success(request,'Your account has been activated successfully')
        else:
            messages.success(request,'تم تفعيل حسابك بنجاح ')
        verification=True
    else:
        verification=False
    data={
        'verification':verification,
        'sendeng_cocunt':sendeng_cocunt,
        'lang':lang,
    }
    return JsonResponse(data)



def resend_msg_active(request):
    email=request.GET.get('email')
    pibszzzz=request.GET.get('pibszzzz')
    tivk=request.GET.get('tivk')
#=========
    uid=urlsafe_base64_decode(pibszzzz).decode()
    user=Accounts._default_manager.get(pk=uid)
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
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
            # mess.send()
            user.validation_code=serial_string
            user.sending_count-=1
            user.right_send= False
            user.save()
        else:
            pass
    sendeng_cocunt=user.sending_count
    data={
        'sendeng_cocunt':sendeng_cocunt,
        'lang':lang,
    }
    return JsonResponse(data)




def LOGIN (request):
    email_value=None
    if 'redilog' in request.GET.get('command', ''):
        if '/en/' in request.path:
            messages.info(request,'This account already exists')
        else:
            messages.info(request,'هذا الحساب موجود بالفعل')
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
            auth.login(request,user)
            return redirect('home')
        else:
            if '/en/' in request.path:
                messages.error(request,'The password is incorrect, If you forgot it click "Forgot password ?"')
            else:
                messages.error(request,'"كلمة المرور غير صحيحة, إذا نسيتها فانقر فوق "هل نسيت كلمة السر ؟"')

            return redirect('login')
        
    return render(request,'registration/login.html',{'email_value':email_value})





def login_fuction(request):
    email=request.GET.get('email')
    is_exist=Accounts.objects.filter(email__iexact=email).exists()
    data={
        "is_exist":is_exist,
    }
    return JsonResponse(data)


def INPUT_EMAIL_PASS (request):
    if request.method == 'POST':
        try:
            email=request.POST.get('email')
            user=Accounts.objects.get(email__iexact=email)
            if user.is_manual == False :
                if '/en/' in request.path:
                    messages.error(request,'This email is for social media accounts')
                else:
                    messages.error(request,'هذا البريد الإلكتروني خاص بحسابات التواصل الاجتماعي')
            else:
                fseq=urlsafe_base64_encode(force_bytes(user.pk))
                aw=default_token_generator.make_token(user)
                return redirect('/accounts/reset_password/?command=reset_pass&email='+email+'&fseq='+fseq+'&aw='+aw)
        except:
            if '/en/' in request.path:
                messages.error(request,'Please check your email')
            else:
                messages.error(request,'يرجي التحقق من بريدك الإلكتروني')
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
        pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
        tivk=default_token_generator.make_token(user)
        if '/en/' in request.path:
            messages.info(request,'You must activate your account first')
        else:
            messages.info(request,'يجب عليك تفعيل حسابك اولا ')
        return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
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
            # mess.send()
            user.validation_code=serial_string
            user.sending_count-=1
            user.right_send= False
            user.save()
        else:
            pass
        sendeng_cocunt=user.sending_count
        return render(request,'registration/inbut_num_pass.html',{'sendeng_cocunt':sendeng_cocunt,'email':email})


def verification_code (request):
    verification=None
    fseq=request.GET.get('fseq')
    uid=urlsafe_base64_decode(fseq).decode()
    user=Accounts._default_manager.get(pk=uid)
    sendeng_cocunt=user.sending_count
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
    theCode=request.GET.get('theCode')
    if theCode == user.validation_code:
        user.right_send= True
        user.sending_count=5
        user.validation_code=None
        user.save()
        request.session['uid']=uid
        if '/en/' in request.path:
            messages.success(request,'Authentication has been completed, you can change your password now')
        else:
            messages.success(request,'تمت المصادقة، يمكنك تغيير كلمة السر الان')
        verification=True
    else:
        verification=False
    data={
        'verification':verification,
        'sendeng_cocunt':sendeng_cocunt,
        'lang':lang,
    }
    return JsonResponse(data)




def resend_msg_password(request):
    email=request.GET.get('email')
    fseq=request.GET.get('fseq')
    aw=request.GET.get('aw')
    uid=urlsafe_base64_decode(fseq).decode()
    user=Accounts._default_manager.get(pk=uid)
    lang=None
    if '/en/' in request.path:
        lang='en'
    else:
        lang='ar'
#=========
    if user is not None and default_token_generator.check_token(user,aw)  and user.sending_count > 0:
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
        # mess.send()
        user.validation_code=serial_string
        user.sending_count-=1
        user.right_send= False
        user.save()
    else:
        pass
    sendeng_cocunt=user.sending_count
    data={
        'sendeng_cocunt':sendeng_cocunt,
        'lang':lang,
    }
    return JsonResponse(data)



def new_password (request):
    if request.method == 'POST':
        password=request.POST['password']
        conf_password=request.POST['conf_password']
        if password == conf_password:
            if len(password) < 6:
                if '/en/' in request.path:
                    messages.error(request,'Sorry, your password must be at least 6 characters long')
                else:
                    messages.error(request,'عذرا، يجب ان تكون كلمة السر ٦ حروف علي الاقل')
                return redirect('new_password')
            else :
                uid=request.session.get('uid')
                user=Accounts.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                if '/en/' in request.path:
                    messages.error(request,'The password has been changed successfully')
                else:
                    messages.success(request,'تم تغيير كلمة السر بنجاح')
                return redirect('login')
        else:
            if '/en/' in request.path:
                messages.error(request,'Passwords do not match')
            else:
                messages.error(request,'كلمات السر غير متطابقة')
            return redirect('new_password')
    else:
        return render(request,'registration/new_password.html')
    

@login_required(login_url='login')
def LOG_OUT (request):
    auth.logout(request)
    if '/en/' in request.path:
        messages.success(request,'You are logged out')
    else:
        messages.success(request,'تم تسجيل خروجك')
    return redirect('login')




def on_popup (request):
    if request.user.is_authenticated:
        on_=True
    else:
        on_=False
    data={
        "on_":on_
    }
    return JsonResponse (data)


def is_popup(request):
    if request.user.is_authenticated:
        popup=True
    else:
        popup=False
    data={
        "popup":popup
    }
    return JsonResponse(data)

