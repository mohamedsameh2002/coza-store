
from django.db import models
from store.models import Product
from accounts.models import Accounts


# Create your models here.
def random_code ():
    return 'a'



class Cart (models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id
    

class Temporary_cart(models.Model):
    temporary_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.temporary_id
    

class CartItem (models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=20)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField()
    #discount_code=models.ForeignKey(Discount_codes,on_delete=models.PROTECT,null=True,blank=True)
    in_active=models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self) -> str:
        return str (self.product)