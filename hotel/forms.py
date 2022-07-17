from django import forms
from django.contrib.auth.forms import AuthenticationForm

from hotel.models import Customer, Booking, SignIn

"""class used when a user sign up."""
class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['desired_username', 'first_name', 'last_name', 'email']
        
"""class used when a user sign in."""
class SignInForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = SignIn
        fields = ['username']

"""class used when a user books a room slot."""
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'book_from_date', 'book_from_time', 'book_till_time', 'capacity'
            ]
        
'''  
class BookForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['book_from', 'book_till']'''
'''
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['book_from', 'book_till', 'category']
'''

'''        
class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30,widget=forms.PasswordInput(attrs={'name': 'password'}))
'''	
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import AuthenticationForm
'''
class SignupForm(UserCreationForm):
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30,widget=forms.PasswordInput(attrs={'name': 'password'}))
'''
