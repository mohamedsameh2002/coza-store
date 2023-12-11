import random
from django.db import models
from django.urls import reverse
from PIL import Image
import uuid
from accounts.models import Accounts,UserProfile
from ckeditor.fields import RichTextField
from django.db.models import Avg
from django.utils.html import mark_safe


# from specifications.models import Category

# Create your models here.


class Category (models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    category_name_ar=models.CharField(max_length=50,unique=True,null=True)
    def __str__(self):
        return self.category_name


class Customizations (models.Model):
    product=models.ForeignKey('Product',on_delete=models.CASCADE)
    sizes=models.ForeignKey('Size_List',on_delete=models.CASCADE)
    colors=models.ForeignKey('Color_List',on_delete=models.CASCADE)
    stock=models.IntegerField(max_length=10000)
    status=models.BooleanField(default=True)
    class Meta:
        verbose_name_plural='Customizations'
    def __str__(self):
        return str (self.product)
    
    

class Color_List (models.Model):
    color_name=models.CharField(max_length=50)
    color_name_ar=models.CharField(max_length=50)
    color_code=models.CharField(max_length=20)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.color_name
    def color_bg(self):
        return mark_safe(f'<div style="width:15px; height:15px; background-color:{self.color_code}"></div>')

class Size_List (models.Model):
    size_name=models.CharField(max_length=50)
    size_name_ar=models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.size_name

    
def image_upload_one (instance,filename):
    random_namper=random.randint(0,10000000)
    return f"products/one/ {random_namper}.png"
class Product (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=50, unique=True)
    product_name_ar = models.CharField(max_length=50, unique=True,null=True)

    description = RichTextField(null=True)
    description_ar = RichTextField(null=True)


    favorits=models.ManyToManyField(Accounts,null=True,blank=True)

    price = models.IntegerField()

    image = models.ImageField(upload_to=image_upload_one)
    avg_rate=models.DecimalField(decimal_places=1,max_digits=2,default=0.0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    
    def all_likes (self):
        likes=self.favorits.count()
        return likes
    
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.image.path)
        pict=pict.resize((1200,1486))
        pict.save(self.image.path)


    def averegeReview (self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg= float(reviews['average'])
        return avg
    def get_absolute_url(self):
        return reverse("product_details", args=[self.id])
    
        


def image_upload (instance,filename):
    random_namper=random.randint(0,10000000)
    return f"products/multi/ {random_namper}.png"



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






class ReviewRating (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    direction=models.CharField(max_length=5,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str (self.product)

