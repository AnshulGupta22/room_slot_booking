from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from hotel.models import Booking

"""Function to check if the username already exists or not."""
def validate_username(value):
        new = User.objects.filter(username = value)
        if new.count():
            raise ValidationError(
                _('%(value)s already exists'),
                code='already exists',
                params={'value': value},
            )

"""Function to check if the email already exists or not."""
def validate_email(value):
        new = User.objects.filter(email = value)
        if new.count():
            raise ValidationError(
                _('%(value)s already exists'),
                code='already exists',
                params={'value': value},
            )

"""class used when a user sign up."""
class CustomerForm(forms.Form):
    username = forms.CharField(label='Desired Username', max_length=150,
                               validators=[validate_username])
    first_name  = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    email = forms.EmailField(label='Your Email', validators=[validate_email])
    password1 = forms.CharField(label='Enter Password',
                                widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Retype Password',
                                widget=forms.PasswordInput, min_length=8)

    """Function to check if password and retyped password match or not."""
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(
                "Passwords do not match"
            )

"""class used when a user sign in."""
class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    """Function to check if username and password match or not."""
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                "Invalid username / password "
            )

import datetime
from django.utils import timezone

"""Function to convert string to date."""
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    datetime_str = datetime.datetime.strptime(date_time, format).date()
    return datetime_str

"""Function to convert string to time."""
def convert_to_time(date_time):
    format = '%H:%M'
    datetime_str = datetime.datetime.strptime(date_time, format).time()
    return datetime_str

now = timezone.now()

"""class used for booking a time slot."""
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time', 'check_out_time',
                    'person', 'no_of_rooms']

    """Function to check if username and password match or not."""
    """def clean(self):
        cleaned_data = super().clean()

        normal_book_date = cleaned_data.get("check_in_date")
        normal_check_in = cleaned_data.get("check_in_time")

        if (normal_book_date < now.date() or
            (normal_book_date == now.date() and
            normal_check_in < now.time())):

            #self._errors['check_in_date'] = self.error_class([
            #    'You can only book for future.])
            raise ValidationError(
                "You can only book for future."
            )
        return cleaned_data"""
    """Function to check if username and password match or not."""
    def is_valid(self):
        valid = super(BookingForm, self).is_valid()
        # ^ valid is a Boolean

        # Note: added self to cleaned_data.get()
        normal_book_date = self.cleaned_data.get("check_in_date")
        normal_check_in = self.cleaned_data.get("check_in_time")

        if (normal_book_date < now.date() or
            (normal_book_date == now.date() and
            normal_check_in < now.time())):

            valid = False

            # Not sure if this works, or is needed (the "raise" part mostly)
            #   if it doesn't work just add the error to the field instead (see below)
            '''raise ValidationError(
                "You can only book for future."
            )'''

            # You could also add the error msg per field & it will render it
            #   - extra tidbit
            self.add_error('check_in_date', 'You can only book for future.')

        return valid