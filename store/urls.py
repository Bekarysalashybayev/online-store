from django.urls import path

from store.views import *

urlpatterns = [
    path('', index, name='store_index'),
    path('shop', shop, name="shop"),
    path('shop/<int:id>', product, name="product"),
    path('shop/other', shopOther, name="other"),
    path('shop/female', shopFeMale, name="female"),
    path('shop/male', shopMale, name="male"),
    path('blog', blog, name="blog"),
    path('order', orders, name="order"),
    path('order/detail/<int:id>', detail),
    # products
    path('add-product/', admin_add_product, name='add_product'),
    path('products/<int:pk>', update_product, name='update_product'),
    path('products/', admin_products, name='admin_products'),
    # blog
    path('blog-list/', admin_blog_list, name='admin_blog_list'),
    path('add-blog/', add_blog_admin, name='add_blog_admin'),
    path('update-blog/<int:pk>', update_blog_admin, name='update_blog_admin'),
    path('delete-blog-admin/<int:pk>', delete_blog_admin, name='delete_blog_admin'),
    # orders
    path('order-list/', order_list_admin, name='order_list_admin'),
    path('order-detail-list/<int:pk>', order_detail_list_admin, name='order_detail_list'),

]
