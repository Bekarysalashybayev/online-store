from django.contrib import admin

# Register your models here.
from store.models import *

admin.site.register(
    [Status, Category, Product, OrderStatus, Order, OrderDetail, Blog]
)
