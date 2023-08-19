from django.db import models
from django.urls import reverse
from PIL import Image
import uuid
from accounts.models import Accounts

# from specifications.models import Category

# Create your models here.


class Category (models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.category_name


class Color (models.Model):
    color_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    color_code=models.CharField(max_length=20,blank=True)
    class Meta:
        verbose_name_plural='color'
    def __str__(self):
        return self.color_name
    def get_url (self):
        return reverse ('product_by_color',args=[self.slug])
    
    
class Size (models.Model):
    size_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    class Meta:
        verbose_name_plural='size'
    def __str__(self):
        return self.size_name
    
    def get_url (self):
        return reverse ('product_by_size',args=[self.slug])
    

class Product (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    sizes=models.ManyToManyField(Size)
    colors=models.ManyToManyField(Color)
    image = models.ImageField(upload_to='products/one')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.image.path)
        pict=pict.resize((1200,1486))
        pict.save(self.image.path)
    


class ProductGallery (models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    img=models.ImageField(upload_to='products/multi')
    def __str__(self) -> str:
        return self.product.product_name
    
    class Meta:
        verbose_name= 'ProductGallery'
        verbose_name_plural= 'ProductGallery'

    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.img.path)
        pict=pict.resize((1200,1486))
        pict.save(self.img.path)



class Favorite (models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str (self.product)