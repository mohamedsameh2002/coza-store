from django.shortcuts import render,redirect
from cart.models import CartItem
from orders.models import Order,Payment,OrderProduct
import datetime
from store.models import Customizations
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from accounts.models import UserProfile
from discounts.models import Discount_codes
from django.template.loader import get_template
from xhtml2pdf import pisa
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from .tasks import order_completion_message


def MK_ORDER (request,total=0,quantity=0,grand_total=0,tax=0):
    is_valed=False
    curent_user=request.user
    car_items=CartItem.objects.filter(user=curent_user)
    cart_count=car_items.count()
    if cart_count <= 0 :
        return redirect ('store')
    
    for cart_item in car_items:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    #========
    user_profile=UserProfile.objects.get(user=curent_user)
    total_discount=0
    if user_profile.discount_cods.exists():
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
    order=Order.objects.create(
        user=curent_user,
        first_name=request.POST.get('info[1][first_name]'),
        last_name=request.POST.get('info[2][last_name]'),
        email=request.POST.get('info[3][email]'),
        phone=request.POST.get('info[4][phone]'),
        address_line_1=request.POST.get('info[5][address_line_1]'),
        address_line_2=request.POST.get('info[6][address_line_2]'),
        city=request.POST.get('info[7][city]'),
        state=request.POST.get('info[8][state]'),
        country=request.POST.get('info[9][country]'),
        order_note=request.POST.get('info[10][order_note]'),
        order_total=total,
        tax=tax,
        final_total=total+tax,
        ip=request.META.get('REMOTE_ADDR'))
    

    yr=int(datetime.date.today().strftime('%Y'))
    dt=int(datetime.date.today().strftime('%d'))
    mt=int(datetime.date.today().strftime('%m'))
    d=datetime.date(yr,mt,dt)
    current_data=d.strftime('%Y%d%m')
    order_numper=current_data+str(order.id)
    order.order_numper =order_numper
    order.save()

# move the cart items to order product model
    for item in car_items :
        orderproduct=OrderProduct()
        orderproduct.order_id= order.id
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product.id
        orderproduct.size=item.size
        orderproduct.color=item.color
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.save()


    if request.POST.get('button') == 'online':
        url_pyament='/orders/O-payment/?pym-m=oneline&order-num='+order_numper
    else:
        order.payment_method='When Recieving'
        order.is_order=True
        order.save()
        # reduce the quantity of the sold products (decriment th stock)
        car_items=OrderProduct.objects.filter(user=curent_user,order=order)
        for item in car_items:
            try:
                costimiz=Customizations.objects.get(product=item.product,colors=item.color,sizes=item.size)
                costimiz.stock-=item.quantity
                costimiz.save()
            except:
                pass
            if costimiz.stock <= 0:
                costimiz.delete()

        # clear the cart
        CartItem.objects.filter(user=curent_user).delete()

        #remove discounts codes

        codes=UserProfile.objects.get(user=curent_user).discount_cods.values_list('code',flat=True)
        for code in codes:
            Discount_codes.objects.get(code=code).delete()
        url_pyament='/orders/order_complete/?pym-m=when-recieving&order-num='+order_numper

    is_valed=True
    data={
        'is_valed':is_valed,
        'url_pyament':url_pyament,
        }
    return JsonResponse(data)
            





def PAYMENT_PAGE(request,total=0,quantity=0):
    order_number=request.GET.get('order-num')
    user=request.user
    paypal_payment=None
    try:
        order=Order.objects.get(user=user,is_order=False,order_numper=order_number)
        host=request.get_host()
        invoice=uuid.uuid4()
        paypal_checkout={
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':order.order_total,
            'tax':order.tax,
            'item_name':order.full_name(),
            'item_number':order_number,
            'invoice':invoice,
            'currency_code':'USD',
            'notify_url':f"http://{host}{reverse('paypal-ipn')}",
            'return':f"http://{host}{reverse('order_complete')}?pym-m=online&order-num={order_number}&invoice={invoice}",
            'cancel_url':f"http://{host}{reverse('payment-cancel')}",
        }
        paypal_payment=PayPalPaymentsForm(initial=paypal_checkout)
    except:
        return redirect('home')
    return render(request,'orders/patment_page.html',{'paypal':paypal_payment})



def ORDER_COMPLEAT (request):
    order_number=request.GET.get('order-num')
    try:
        order=Order.objects.get(user=request.user,order_numper=order_number,status='Delivery is in progress')
    except:
        return redirect('home')
    return render(request,'orders/order_complete.html')




def CHECK_ORDER (request):
    pyment_method=request.GET.get('pyment_method')
    order_number=request.GET.get('order_number')
    user=request.user
    template=False
    if '/en/' in request.path:lang='en'
    else:lang='ar'
    if pyment_method == 'online':
        invoice=request.GET.get('invoice')
        payerID=request.GET.get('payerID')
        try:
            order=Order.objects.get(user=user,order_numper=order_number,is_order=True)
            order_products=OrderProduct.objects.filter(order__id=order.id)
            payment=Payment.objects.get(payer_id=payerID,invoice_id=invoice,user=user)
        except (Payment.DoesNotExist,Order.DoesNotExist):
            order_products=None
            order=None
            payment=None
    else:
        try:
            order=Order.objects.get(user=user,order_numper=order_number,is_order=True)
            order_products=OrderProduct.objects.filter(order__id=order.id)
            payment=None
            #start send th messge
            if order.order_E_mesg == False:
                id=user.id
                order_completion_message.delay(id,order_number,lang)
            # end send the mesgge
        except:
            return redirect('home')
    if order_products:
        subtotal=0
        for i in order_products :
            subtotal += i.product_price * i.quantity
    context={
        'order':order,
        'order_products':order_products,
        'order_number':order_number,
        'subtotal':subtotal,
        'payment':payment,
        'lang':lang,
    }
    template=render_to_string('orders/ajax/order_complete_aj.html',context)
        
    
    data={
        'template':template,
    }
    return JsonResponse(data)


def payment_cancel(request):
    return HttpResponse('worng')







    



def GENERATE_INVOICE (request,order_number):
    order=Order.objects.get(user=request.user,order_numper=order_number,is_order=True)
    order_products=OrderProduct.objects.filter(order__id=order.id)
    total=0
    for i in order_products :
        total += i.product_price * i.quantity
    total_discount=0
    if request.user.is_authenticated:
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        if user_profile.discount_cods.exists():
            # codes=user_profile.discount_cods.all()
            codes=user_profile.discount_cods.values_list('code',flat=True)
            for code in codes:
                discount=Discount_codes.objects.get(code=code).discount
                total_discount+=discount
            if total < total_discount:
                total=0
            else :
                total = total - total_discount

    template_path = 'includes/invoice.html'
    context = {'order_products': order_products,'order':order,'total':total}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    # response['Content-Disposition'] = 'filename="report.svg"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

