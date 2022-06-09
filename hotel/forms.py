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
from hotel.models import Hotel, Room, Booking
from django import forms

class HotelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Hotel
        fields = ['username', 'first_name', 'last_name', 'email']
        
class SigninForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Hotel
        fields = ['username']
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['book_from', 'book_till']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['book_from', 'book_till', 'category']
        
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import AuthenticationForm
'''
class SignupForm(UserCreationForm):
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30,widget=forms.PasswordInput(attrs={'name': 'password'}))
'''
