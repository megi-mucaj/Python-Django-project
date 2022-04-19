from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shitje_online.models import Employee



class EmpForm(forms.ModelForm):
    class Meta:
        model = Employee
       fields = "__all__"







class CreateUserForm(UserCreationForm):
    class Meta:
        models = User
        fields =['username', 'email', 'password1', 'password2']






