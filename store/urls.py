from django.urls import path

from store.views import *

urlpatterns = [
    path('', index, name='store_index'),
    path('shop', shop),
    path('shop/other', shopOther),
    path('shop/female', shopFeMale),
    path('shop/male', shopMale),
    path('blog', blog),
    path('order', orders),
    path('order/detail/<int:id>', detail),
]
