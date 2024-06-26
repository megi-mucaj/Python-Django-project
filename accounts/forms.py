from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order
from django import forms


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

# it means that we want all fields of Order module to be filled


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


