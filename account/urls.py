from django.urls import path

from account.views import *

urlpatterns = [
    path('logining', logining, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register', register, name="register"),
    path('code/<int:pk>/', code, name='code'),
    path('admin-panel/', code, name='admin-panel'),
    path('user-update/<int:pk>', update_user, name='user_update_panel'),
]
