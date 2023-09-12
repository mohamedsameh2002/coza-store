from django.db import models
from PIL import Image

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class MyAccountsManager (BaseUserManager):
    def create_user (self,first_name,last_name,username,email,phone_numper,profile_pictuer,password=None):
        if not email :
            raise ValueError('User Mast Have A Email')
        if not username:
            raise ValueError('User Mast Have A Username')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_numper=phone_numper,
            profile_pictuer=profile_pictuer,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
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
        user.is_superadmin=True
        user.save(using=self._db)
        return user

class Accounts(AbstractBaseUser):
    first_name =models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    username =models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    phone_numper=models.CharField(max_length=50)
    address_line_1=models.CharField(max_length=100,blank=True)
    address_line_2=models.CharField(max_length=100,blank=True)
    profile_pictuer=models.ImageField(upload_to='userprofile',null=True,blank=True)
    city=models.CharField(max_length=20,blank=True)
    state=models.CharField(max_length=20,blank=True)
    country=models.CharField(max_length=20,blank=True)

    # Confirmation messages
    session_code=models.CharField(max_length=250,null=True,blank=True)
    validation_code=models.CharField(max_length=10,null=True,blank=True)
    sending_count=models.IntegerField(null=True,blank=True,default=5)
    right_send=models.BooleanField(default=True)

    #required
    dete_joined   =models.DateTimeField(auto_now_add=True)
    last_login =models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    is_staff =models.BooleanField(default=False)
    is_admin =models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name',]
    objects=MyAccountsManager()

    def __str__(self):
        return self.email
    
    def has_perm (self,perm,obj=None):
        return self.is_admin
    
    def full_address (self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def has_module_perms (self,add_label):
        return True
    
    def save (self,*args,**kwargs): 
        super().save(*args,**kwargs)
        pict=Image.open(self.profile_pictuer.path)
        pict=pict.resize((1200,1486))
        pict.save(self.profile_pictuer.path)
    


# class UserProfile (models.Model):
#     user=models.OneToOneField(Accounts,on_delete=models.CASCADE)
#     address_line_1=models.CharField(max_length=100,blank=True)
#     address_line_2=models.CharField(max_length=100,blank=True)
#     profile_pictuer=models.ImageField(upload_to='userprofile',null=True,blank=True)
#     city=models.CharField(max_length=20,blank=True)
#     state=models.CharField(max_length=20,blank=True)
#     country=models.CharField(max_length=20,blank=True)
#     def __str__(self) -> str:
#         return self.user.first_name
#     def full_address (self):
#         return f'{self.address_line_1} {self.address_line_2}'
