from django.shortcuts import render,redirect
from cart.models import CartItem
from.forms import OrderForm
from orders.models import Order,Payment,OrderProduct
import datetime
import json
from store.models import Product,Customizations
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
from accounts.models import UserProfile
from discounts.models import Discount_codes


def PAYMENTES (request):
    body = json.loads(request.body)
    # print(body)
    order=Order.objects.get(user=request.user,is_order=False,order_numper=body['orderID'])
    # store transaction details inside payment model
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method= body['payment_method'],
        amount_paid = order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment=payment
    order.is_order=True
    order.save()
    # move the cart items to order product model
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items :
        orderproduct=OrderProduct()
        orderproduct.order_id= order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.size=item.size
        orderproduct.color=item.color
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        

    # reduce the quantity of the sold products (decriment th stock)
    costimiz=Customizations.objects.get(product=item.product,colors=item.color,sizes=item.size)
    costimiz.stock-=item.quantity
    costimiz.save()
    if costimiz.stock <= 0:
        costimiz.delete()

    # clear the cart
    CartItem.objects.filter(user=request.user).delete()

    #remove discounts codes
    try:
        codes=UserProfile.objects.get(user=request.user).discount_cods.values_list('code',flat=True)
        for code in codes:
            Discount_codes.objects.get(code=code).delete()
    except:
        pass
    

    # send order received email to customer
    mail_supject='thank u for your order!'
    message=render_to_string('orders/order_received_email.html',{
        'user':request.user,
        'order':order,
    })
    to_email=request.user.email 
    send_email=EmailMessage(mail_supject,message,to=[to_email])
    send_email.send()

    data={
        'order_number':order.order_numper,
        'transID':payment.payment_id,
    }

    #Look at the javascript code at the end of the payments.html page
    return JsonResponse(data)






def GO_PYMENT (request,total=0,quantity=0):
    curent_user=request.user
    car_items=CartItem.objects.filter(user=curent_user)
    cart_count=car_items.count()
    if cart_count <= 0 :
        return redirect ('store')
    grand_total=0
    tax=0
    for cart_item in car_items:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax

    #========
    user_profile=UserProfile.objects.get(user=curent_user)
    if user_profile.discount_cods.exists():
        total_discount=0
        codes=user_profile.discount_cods.values_list('code',flat=True)
        for code in codes:
            discount=Discount_codes.objects.get(code=code).discount
            total_discount+=discount
        if total < total_discount:
            total=0
            grand_total=tax
        else :
            total = total - total_discount
            grand_total=total+tax
    #========

    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=curent_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            #generate order number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_data=d.strftime('%Y%d%m')
            order_numper=current_data+str(data.id)
            data.order_numper =order_numper
            data.save()
            order=Order.objects.get(user=curent_user,is_order=False,order_numper=order_numper)
            context={
                'order':order,
                'cart_items':car_items,
                'tax':tax,
                'grand_total':grand_total,
                'total':total,
            }
            return render(request,'orders/paymentes.html',context)
    else:
        return redirect('chekout')
    





def ORDER_COMPLEAT (request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_numper=order_number,is_order=True)
        order_products=OrderProduct.objects.filter(order_id=order.id)
        
        subtotal=0
        for i in order_products :
            subtotal += i.product_price * i.quantity


        payment=Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'order_products':order_products,
            'order_number':order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render (request,'Orders/order_complete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect ('home')
    