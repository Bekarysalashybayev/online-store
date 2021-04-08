from django.urls import path

from account.views import *

urlpatterns = [
    path('logining', logining),
    path('register', register),
    path('code/<int:pk>/', code, name='code'),
    path('admin-panel/', code, name='admin-panel'),
]
