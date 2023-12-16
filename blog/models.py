import random
from django.db import models
from accounts.models import UserProfile,Accounts
from PIL import Image
from store.models import Product
from taggit.managers import TaggableManager


# Create your models here.
class Category (models.Model):
    category=models.CharField(max_length=100)
    category_ar=models.CharField(max_length=100,null=True)
    
    criated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.category
    


# def image_upload (instance,filename):
#     random_namper=random.randint(0,10000000)
#     return f"blog/ {random_namper}.jpg"
class Blog (models.Model):
    publisher=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True)
    topic=models.CharField(max_length=300,unique=True)
    content=models.TextField()
    topic_ar=models.CharField(max_length=300,unique=True,null=True)
    content_ar=models.TextField()

    tags=TaggableManager()
    image=models.ImageField(upload_to='blog')
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
    def commetns_count(self):
        comments=Comments.objects.filter(post=self).count()
        replis=Reply.objects.filter(post=self).count()
        return comments + replis
        
    


class Comments(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment=models.TextField(max_length=2000, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return str (self.post)
    def is_has_reply(self):
        is_rplay=Reply.objects.filter(comment=self).exists()
        return is_rplay
    def count_reply(self):
        count=Reply.objects.filter(comment=self).count()
        return count
    

class Reply(models.Model):
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.TextField(max_length=2000, blank=True)
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='rply_for_rply')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_date)
    def reply_or_comment(self):
        if self.parent_reply != None:
            return self.parent_reply.user.user.full_name()
        else:
            return self.comment.user.user.full_name()


class Notification(models.Model):
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    reply_sent = models.ForeignKey(Accounts, on_delete=models.CASCADE,related_name='sender')
    reply_recipient = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)