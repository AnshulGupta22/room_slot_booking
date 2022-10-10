from django import forms
#from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from hotel.models import Booking

"""class used when a user sign up."""

def validate_username(value):
        new = User.objects.filter(username = value)  
        if new.count():
            raise ValidationError(
                _('%(value)s already exists'),
                params={'value': value},
            )

def validate_email(value):
        new = User.objects.filter(email = value)  
        if new.count():
            raise ValidationError(
                _('%(value)s already exists'),
                params={'value': value},
            )

class CustomerForm(forms.Form):
    username = forms.CharField(label='Desired Username', max_length=150, validators=[validate_username])
    first_name  = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    email = forms.EmailField(label='Your Email', validators=[validate_email])
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Retype Password', widget=forms.PasswordInput, min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError(
                "Passwords do not match"
            )

    '''def save(self, commit = True):
        try:
            user = User.objects.create_user(
                self.username,
                self.email, self.password1
            )
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.save()
        except Exception:
            return #HttpResponse("Username/ E-mail already exist")'''

"""class used when a user sign in."""
class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                "Invalid username / password "
            )

'''
class SignInForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = SignIn
        fields = ['username']'''

"""class used when a user books a room slot."""
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time', 'check_out_time', 
                    'person', 'no_of_rooms']
