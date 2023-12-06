from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from django.apps import apps
from django.utils import timezone

from django.utils.text import slugify
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):

    """ Main User config """
    email = models.EmailField(unique=True, verbose_name='Email Address')
    username = models.CharField(max_length=256)
    # user_name = models.CharField(max_length=255)
    # date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    SUPERUSER = '1'
    VENDER = '2'
    ADDUSER = '3'
    BLOGER = '4'
   
   
    User_type=(
        ('Superuser','SUPERUSER'),
      
        ('AddUser','ADDUSER'),
        ('Vender','VENDER'),
        ('Bloger','BLOGER'),
               
    )
    user_type_data = (('Bloger','BLOGER'), ( VENDER, "Vender"), (ADDUSER, "AddUser"), (SUPERUSER, "Superuser"))
    user_type = models.CharField( choices=user_type_data, max_length=10,default='1')
 
       
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):

        return f'{self.username} '

    def has_perm(self, perm, obj=None):
        # User permission
        return True

    def has_module_perms(self, app_label):
        # User permission to view the ap modules
        return True



class Country(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class State(models.Model):
    country=models.ForeignKey(Country, on_delete=models.CASCADE,default=1)
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AddUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField()
    # gender=models.CharField(max_length=100)
    contact=models.IntegerField()
    profile_pic=models.ImageField(upload_to='user_profile',default="")
    city=models.CharField(max_length=100)
    # password=models.CharField(max_length=100)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = ('adduser')
        verbose_name_plural = ('adduser')

    def save(self, *args, **kwargs):

        self.slug = slugify(self.user.username )
        return super().save(*args, **kwargs)
    def __str__(self):

        return f"{self.user}"


class Vender(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField()
    # gender=models.CharField(max_length=100)
    contact=models.IntegerField()
    profile_pic=models.ImageField(upload_to='user_profile',default="")
    city=models.CharField(max_length=100)
    # password=models.CharField(max_length=100)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = ('vender')
        verbose_name_plural = ('vender')

    def save(self, *args, **kwargs):

        self.slug = slugify(self.user.username )
        return super().save(*args, **kwargs)
    def __str__(self):

        return f"{self.user}"


class Blogger(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField()
    contact=models.IntegerField()
    profile_pic=models.ImageField(upload_to='user_profile',default="")
    city=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = ('bloger')
        verbose_name_plural = ('bloger')

    def save(self, *args, **kwargs):

        self.slug = slugify(self.user.username )
        return super().save(*args, **kwargs)
    def __str__(self):

        return f"{self.user}"




#///////////// for products //////////////

class Blog(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    title=models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic=models.ImageField(upload_to='blog',default="")



#///////////// for products //////////////

class Category(models.Model):
    name = models.CharField(max_length=200)
    image=models.ImageField(upload_to='category_img',default="")

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    image = models.ImageField(upload_to='products')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()


    def __str__(self):
        return self.name



# ////////////////add to cart and checkout/////////////////

# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     country=models.ForeignKey(Country, on_delete=models.CASCADE)
#     state=models.ForeignKey(State, on_delete=models.CASCADE)
#     city=models.ForeignKey(City, on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)

class Adres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100,null=True, blank=True)
    # city=models.ForeignKey(City, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.street_address

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price
    
  
    def image_url(self):
        return self.product.image.url




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(Adres, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,default='pending')

    # def __str__(self):
    #     return self.order
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order
        

class CancelReason(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    
    def __str__(self):
        return self.reason  

# gpt this is my checkout page's design and i have to follow these all fields so is it possible that in this form i can fetch user's details  as value in input field and if user choose ship to the address then it is click


