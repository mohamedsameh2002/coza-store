import random
from django.db import models
from accounts.models import UserProfile
from PIL import Image
from store.models import Product

# Create your models here.
class Category (models.Model):
    category=models.CharField(max_length=100)
    category_ar=models.CharField(max_length=100,null=True)
    
    criated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.category
    
class Tags (models.Model):
    blog=models.ForeignKey('Blog',on_delete=models.CASCADE)
    tag=models.CharField(max_length=50)
    tag_ar=models.CharField(max_length=50,null=True)
    
    criated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.tag


def image_upload (instance,filename):
    random_namper=random.randint(0,10000000)
    return f"blog/ {random_namper}.jpg"
class Blog (models.Model):
    publisher=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True)
    topic=models.CharField(max_length=300,unique=True)
    topic_ar=models.CharField(max_length=300,unique=True,null=True)
    
    content=models.TextField()
    content_ar=models.TextField()

    image=models.ImageField(upload_to=image_upload)
    p_products=models.ManyToManyField(Product,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.image.path)
        pict=pict.resize((1200,601))
        pict.save(self.image.path)

    def __str__(self) -> str:
        return self.topic