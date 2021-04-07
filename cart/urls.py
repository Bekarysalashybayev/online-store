from django.urls import path

from cart.views import *

app_name = 'cart'


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('checkout', checkout, name='cart_checkout'),
    path('clear/', cart_clear, name='cart_clear'),
    path('add/<int:product_id>/',
         cart_add,
         name='cart_add'),
    path('remove/<int:product_id>/',
         cart_remove,
         name='cart_remove'),
]