from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    slug = models.CharField(max_length=300,unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.CharField(max_length=300,unique=True)

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Ad(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank=True)
    rank = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media')
    rank = models.IntegerField(unique=True)
    slug = models.CharField(max_length=200,unique=True)
    def __str__(self):
        return self.name
STOCK = (('Instock','Instock'),('Outstock','Outstock'))
LABELS = (('hot','Hot'),('new','New'),('sale','Sale'),('','default'))

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=200,unique=True)
    price = models.IntegerField()
    discounted_price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stock = models.CharField(choices=STOCK,max_length=200)
    label = models.CharField(choices=LABELS, max_length=200)
    def __str__(self):
         return self.name

class Review(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=300)
    email = models.EmailField(max_length=200)
    comment = models.TextField(blank=True)
    star = models.IntegerField(default=1)
    date = models.CharField(max_length=200)

class Cart(models.Model):
    username = models.CharField(max_length=300)
    quantity = models.IntegerField()
    total = models.IntegerField()
    items = models.ForeignKey(Product,on_delete=models.CASCADE)
    slug = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name =  models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address =  models.CharField(max_length=200)
    city =  models.CharField(max_length=200)
    state =  models.CharField(max_length=200)
    country =  models.CharField(max_length=200)
    post_code = models.IntegerField()
    phone = models.IntegerField()
    amount = models.CharField(max_length=300)
    payment_id = models.CharField(max_length=200,null=True,blank=True)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Orderitem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return order.user.username

