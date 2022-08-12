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
        fields = ['book_from_date', 'book_from_time', 'book_till_time', 
                    'capacity']

