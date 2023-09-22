import random
from django.db import models
from django.urls import reverse
from PIL import Image
import uuid
from accounts.models import Accounts,UserProfile
from ckeditor.fields import RichTextField

# from specifications.models import Category

# Create your models here.


class Category (models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    category_name_ar=models.CharField(max_length=50,unique=True,null=True)
    def __str__(self):
        return self.category_name


class Color (models.Model):
    color_name=models.CharField(max_length=50,unique=True)
    color_name_ar=models.CharField(max_length=50,unique=True,null=True)

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
    size_name_ar=models.CharField(max_length=50,unique=True,null=True)
    
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
    product_name_ar = models.CharField(max_length=50, unique=True,null=True)

    description = RichTextField(null=True)
    description_ar = RichTextField(null=True)

    information=RichTextField(null=True)
    information_ar=RichTextField(null=True)

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
    
    def all_likes (self):
        likes=Favorite.objects.filter(product=self).exclude(user=None).count()
        return likes
    
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.image.path)
        pict=pict.resize((1200,1486))
        pict.save(self.image.path)
    

def image_upload (instance,filename):
    random_namper=random.randint(0,10000000)
    return f"products/multi/ {random_namper}.jpg"
class ProductGallery (models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    img=models.ImageField(upload_to=image_upload)
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

class Favorite_storeg_id (models.Model):
    favorite_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.favorite_id

class Favorite (models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    by_session=models.ForeignKey(Favorite_storeg_id,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    # favorit_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str (self.product)



class ReviewRating (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str (self.product)

