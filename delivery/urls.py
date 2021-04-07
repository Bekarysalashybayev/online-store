from django.urls import path

from delivery.views import *

urlpatterns = [
    path('', admin_base),
]