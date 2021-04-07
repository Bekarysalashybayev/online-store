from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'phone',  'icon']
