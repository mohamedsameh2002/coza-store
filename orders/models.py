from django.db import models
from accounts.models import Accounts
from store.models import Product,Color_List,Size_List


# Create your models here.

class Payment (models.Model):
    user=models.ForeignKey(Accounts, on_delete=models.CASCADE)
    payer_id=models.CharField(max_length=100)
    method=models.CharField(max_length=20)
    invoice_id=models.CharField(max_length=200,null=True)
    amount=models.CharField(max_length=100)
    receiver_id=models.CharField(max_length=200,null=True)
    transaction_id=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return str (self.transaction_id)


class Order (models.Model):
    PAYMENT_METHODS=[
        ('When Recieving','When Recieving'),
        ('Paypal','Paypal'),
        ('Stripe','Stripe'),
        ('None','None'),
    ]
    STATUS=[
        ('Delivered','Delivered'),
        ('Delivery is in progress','Delivery is in progress'),
    ]
    user=models.ForeignKey(Accounts, on_delete=models.SET_NULL,null=True)
    payment_method=models.CharField(max_length=15,choices=PAYMENT_METHODS,default='None')
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    order_numper=models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=100,blank=True)
    tax=models.FloatField()
    order_total=models.FloatField()
    final_total=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    is_order=models.BooleanField(default=False)
    status=models.CharField(choices=STATUS,max_length=100,default='Delivery is in progress')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    order_E_mesg=models.BooleanField(default=False)

    def full_name (self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address (self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self) -> str:
        return self.first_name
    

class OrderProduct(models.Model):
    user=models.ForeignKey(Accounts, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    color=models.ForeignKey(Color_List,on_delete=models.CASCADE,null=True)
    size=models.ForeignKey(Size_List,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.product.product_name
    def sub_total(self):
        return self.product.price * self.quantity
