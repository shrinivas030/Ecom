from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=20,null=True)
    phone=models.CharField(max_length=10,null=True)
    email=models.EmailField(max_length=30,null=True)
    profile_pic=models.ImageField(default='profile1.png',)
    date_created=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGOLRY=(
        ('indoor','indoor'),
        ('outdoor','outdoor'),
                 )
    name=models.CharField(max_length=25)
    price=models.FloatField(null=True)
    catagory=models.CharField(max_length=25,choices=CATEGOLRY)
    description=models.CharField(max_length=50)
    date_created=models.DateField(auto_now_add=True,null=True)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
        ('Delivered','Delivered'),
        ('pending','pending'),
        ('out of delivery','out of delivery'),
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_of_created=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=25,choices=STATUS)
    note=models.CharField(max_length=225,null=True)

    def __str__(self):
        return self.product.name

