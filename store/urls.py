from django.urls import path

from store.views import *

urlpatterns = [
    path('', index),
    path('shop', shop, name="shop"),
    path('shop/<int:id>', product, name="product"),
    path('shop/other', shopOther, name="other"),
    path('shop/female', shopFeMale, name="female"),
    path('shop/male', shopMale, name="male"),
    path('blog', blog, name="blog"),
    path('order', orders, name="order"),
    path('order/detail/<int:id>', detail),
]
