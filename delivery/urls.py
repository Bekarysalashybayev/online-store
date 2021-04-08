from django.urls import path

from delivery.views import *

urlpatterns = [
    path('', admin_base, name="delivery"),
    path('profile', profile, name="profile"),
    path('orders', orders, name="orders"),
    path('orders/<int:id>', getorders, name="getorders"),
    path('orders/my', myorders, name="myorders"),
    path('orders/my/<int:id>', deliveryorders, name="deliveryorders"),
    path('orders/my/<int:id>/finish', orderfinish, name="orderfinish"),
]