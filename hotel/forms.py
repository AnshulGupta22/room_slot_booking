'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
	model = User
	fields = ["username", "email", "password1", "password2"]
'''
from hotel.models import Hotel
from django import forms

class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = ['username','email', 'password']

#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import AuthenticationForm
'''
class SignupForm(UserCreationForm):
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30,widget=forms.PasswordInput(attrs={'name': 'password'}))
'''
