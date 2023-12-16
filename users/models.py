import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from .validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password, **extra_fields):
        
        email=self.normalize_email(email)
        user = self.model(email=email,**extra_fields)

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")
        
        self.create_user(email,password,**extra_fields)

class Coordinate(models.Model):
    latitude=models.FloatField()
    longitude=models.FloatField()
    address=models.CharField(max_length=255)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    #Basic info
    email=models.EmailField(max_length=254, unique=True, validators=[validate_email])
    #password=models.CharField(max_length=128,null=True)
    phone=models.CharField(max_length=255,null=True,blank=True, validators=[validate_phone])
    username=models.CharField(max_length=255,null=True,blank=True, validators=[validate_username])
    first_name=models.CharField(max_length=255,null=True,blank=True, validators=[validate_name])
    last_name=models.CharField(max_length=255,null=True,blank=True, validators=[validate_name])
    photo=cloudinary.models.CloudinaryField('media/user/', overwrite=True, resource_type='',null=True,blank=True)

    #Permissions
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    #Important dates
    last_login=models.DateTimeField(null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    
    #Extra info
    coordinate=models.OneToOneField(Coordinate,on_delete=models.CASCADE,null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['phone','username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self,app_label):
        return True
    
    def has_perm(self,perm,obj=None):
        return True
    
class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)


class Worker(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    is_available=models.BooleanField(default=True)
    rating=models.FloatField(default=0.0)
