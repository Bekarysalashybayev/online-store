from django.urls import path

from account.views import *

urlpatterns = [
    path('logining', logining, name="login"),
    path('register', register, name="register"),
    path('code/<int:pk>/', code, name='code'),
    path('admin-panel/', code, name='admin-panel'),
]
