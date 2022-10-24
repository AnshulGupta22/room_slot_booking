from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime

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
                _("Passwords do not match"),
                code='Passwords do not match'
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
                _("Invalid username / password"),
                code='invalid'
            )

"""Function to convert string to date."""
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_time, format).date()
    except Exception:
        raise ValidationError(
                "Wrong date format entered.", code='Wrong date format'
            )

"""Function to convert string to time."""
def convert_to_time(value):
    format = '%H:%M:%S'
    try:
        print("dsgji")
        datetime.datetime.strptime(value, format).time()
    except Exception:
        print("qkftio")
        raise ValidationError(
            _('%(value)s Wrong time format entered.'),
            code='Wrong time format entered.',
            params={'value': value},
        )

"""Function to check if the email already exists or not."""
def validate_check_in_time(value):
    format = '%H:%M:%S'
    try:
        print("bhjkkq")
        datetime.datetime.strptime(value, format).time()
    except Exception:
        print("qkftio")
        raise ValidationError(
            _('%(value)s Wrong time format entered.'),
            code='Wrong time format entered.',
            params={'value': value},
        )

"""class used for booking a time slot."""
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time', 'check_out_time',
                    'person', 'no_of_rooms']

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        normal_book_date = cleaned_data.get("check_in_date")
        normal_check_in = cleaned_data.get("check_in_time")
        normal_check_out_time = cleaned_data.get("check_out_time")
        #validate_check_in_time(str(normal_check_in))
        #ghj = str(normal_check_in)


        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (normal_book_date < now.date() or
            (normal_book_date == now.date() and
            normal_check_in < now.time())):
            raise ValidationError(
                "You can only book for future.", code='only book for future'
            )
        if not normal_check_out_time > normal_check_in:
            raise ValidationError(
                "Check out should be after check in.", code='check out after check in'
            )

    def is_valid(self):
            valid = super(BookingForm, self).is_valid()
            # ^ Boolean value

            format = '%H:%M:%S'
            try:
                # Note: `self.cleaned_date.get()`
                #print(type(self.cleaned_data.get('check_in_time')))
                sdf = str(self.cleaned_data.get('check_in_time'))
                datetime.datetime.strptime(sdf, format).time()
            except Exception:

                self.add_error('check_in_time', 'Wrong time format entered.')
                valid = False

            return valid