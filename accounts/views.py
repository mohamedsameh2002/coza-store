import random
import string
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages,auth
from cart.models import Cart,CartItem
from cart.views import _cart_id
from store.models import Product,Favorite
from store.views import _favorit_id
from accounts.models import Accounts
from .forms import SingupForm
from django.conf import settings
from django.utils.html import strip_tags


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives


def SINGUP (request):
    
    if request.method == 'POST':
        form=SingupForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_numper=form.cleaned_data['phone_numper']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            profile_pictuer=form.cleaned_data['profile_pictuer']
            password=form.cleaned_data['password']
            user=Accounts.objects.create_user(first_name=first_name,last_name=last_name,phone_numper=phone_numper,email=email,username=username,password=password,profile_pictuer=profile_pictuer)
            user.is_staff=True
            user.save()
            pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
            tivk=default_token_generator.make_token(user)
            return redirect('/accounts/active/?command=activation&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
        else:
            email=request.POST.get('email')
            is_exist=Accounts.objects.filter(email__exact=email).exists()
            if is_exist:
                user=Accounts.objects.get(email__exact=email)
                pibszzzz=urlsafe_base64_encode(force_bytes(user.pk))
                tivk=default_token_generator.make_token(user)
                return redirect('/accounts/login/?command=redilog&email='+email+'&pibszzzz='+pibszzzz+'&tivk='+tivk)
    return render(request,'registration/singup.html')

def activation_account (request):
    email=request.GET.get('email')
    pibszzzz=request.GET.get('pibszzzz')
    tivk=request.GET.get('tivk')
    # session=request.session.session_key
    # print(session)
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
                user.sending_count=5
                user.right_send= True
                user.save()
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
                            car=Cart.objects.all().delete()
            except:
                pass
            is_exist_favorit=Favorite.objects.filter(by_session=_favorit_id(request)).exists()
            if is_exist_favorit:
                favorits=Favorite.objects.filter(by_session=_favorit_id(request))
                for fav in favorits:
                    fav_product=Product.objects.get(id=fav.product.id)
                    isfav_ex_inuser=Favorite.objects.filter(user=user,product=fav_product).exists()
                    if isfav_ex_inuser :
                        x=Favorite.objects.get(by_session=_favorit_id(request),product=fav_product)
                        x.delete()
                    else:
                        fav.user=user
                        fav.by_session=None
                        fav.save()
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
