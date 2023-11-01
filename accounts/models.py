import random
import string
from django.db import models
from PIL import Image
from discounts.models import Discount_codes
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.utils.html import mark_safe
from django.contrib import auth

# Create your models here.

class MyAccountsManager (BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        if email:
            pass
        else:
            all_chars = string.ascii_letters + string.digits 
            serial_list = [random.choice(all_chars) for _ in range(8)]
            serial_string = ''.join(serial_list)
            email=f'{serial_string}@mkusr.net'

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    


    def create_superuser (self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    

def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions

class Accounts(AbstractBaseUser):
    first_name =models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    username =models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    

    # Confirmation messages
    validation_code=models.CharField(max_length=10,null=True,blank=True)
    sending_count=models.IntegerField(null=True,blank=True,default=5)
    is_manual=models.BooleanField(default=False)
    right_send=models.BooleanField(default=False)

    #required
    dete_joined   =models.DateTimeField(auto_now_add=True)
    last_login =models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_staff =models.BooleanField(default=False)
    is_admin =models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name',]
    objects=MyAccountsManager()
    

    def __str__(self):
        return self.email
    
    def full_name (self):
        return f'{self.first_name} {self.last_name}'
    
    def has_perm (self,perm,obj=None):
        return self.is_admin
    
    
    def has_module_perms (self,add_label):
        return True
    
    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")
    



def image_upload (instance,filename):
    random_namper=random.randint(0,10000000)
    return f"userprofile/ {random_namper}.jpg"
class UserProfile (models.Model):
    user=models.OneToOneField(Accounts,on_delete=models.CASCADE)
    phone_numper=models.CharField(max_length=50,null=True,blank=True)
    address_line_1=models.CharField(max_length=100,blank=True)
    address_line_2=models.CharField(max_length=100,blank=True)
    profile_pictuer=models.ImageField(upload_to=image_upload,null=True,blank=True,default='userprofile/7603668.jpg')
    city=models.CharField(max_length=20,blank=True)
    state=models.CharField(max_length=20,blank=True)
    country=models.CharField(max_length=20,blank=True)
    discount_cods=models.ManyToManyField(Discount_codes,null=True,blank=True)
    def __str__(self) -> str:
        return self.user.first_name
    def full_address (self):
        return f'{self.address_line_1} {self.address_line_2}'

    def image_tag(self):
        return mark_safe(f'<img src="{self.profile_pictuer.url}" width="30" style="border-radius:50%;/>"')
    
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.profile_pictuer.path)
        pict=pict.resize((960,960))
        pict.save(self.profile_pictuer.path)

    def full_address (self):
        return f'{self.address_line_1} {self.address_line_2}'