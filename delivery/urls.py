from django.urls import path

from delivery.views import *

urlpatterns = [
    path('', admin_base),
    path('orders', orders, name="orders"),
    path('orders/<int:id>', getorders, name="getorders"),
    path('orders/my', myorders, name="myorders"),
    path('orders/my/<int:id>', deliveryorders, name="deliveryorders"),
]