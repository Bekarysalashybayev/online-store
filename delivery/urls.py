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
    path('deliveries/', admin_deliveries, name="deliveries_list"),
    path('<int:pk>/', admin_update_deliveries, name="admin_update_deliveries_list"),
    path('add-deliveries/', admin_add_deliveries, name="add_deliveries"),
    path('delete-deliverie/<int:id>', delete_delivery, name="delete_delivery"),
    path('delete-product/<int:id>', delete_product, name="delete_product"),
]