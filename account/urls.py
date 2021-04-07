from django.urls import path

from account.views import *

urlpatterns = [
    path('logining', logining),
    path('register', register),
]
