from django.db import models

from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255)
    percent = models.FloatField(default=0)

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    img1 = models.ImageField(upload_to='images/', blank=True, null=True)
    img2 = models.ImageField(upload_to='images/', blank=True, null=True)
    img3 = models.ImageField(upload_to='images/', blank=True, null=True)
    img4 = models.ImageField(upload_to='images/', blank=True, null=True)
    img5 = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.CharField(max_length=50, blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, blank=True, null=True, default=1)
    delivery = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='delivery',
                                 verbose_name='delivery')

    def __str__(self):
        return self.user.name


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.CharField(max_length=50, blank=True, null=True)
    count = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.order.user.name + " " + self.product.name
