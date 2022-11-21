from email.policy import default
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime
from django.core.validators import int_list_validator, MaxValueValidator, MinValueValidator, validate_slug

from hotel.models import Booking, Room

"""Function to check if the username already exists or not."""
def validate_username(value):
    new = User.objects.filter(username=value)
    if new.count():
        raise ValidationError(
            _('%(value)s already exists'),
            code='already exists',
            params={'value': value},
        )

"""Function to check if the email already exists or not."""
def validate_email(value):
    new = User.objects.filter(email=value)
    if new.count():
        raise ValidationError(
            _('%(value)s already exists'),
            code='already exists',
            params={'value': value},
        )

"""class used when a user sign up."""
class CustomerForm(forms.Form):
    username = forms.CharField(label='Desired Username', max_length=150,
                               validators=[validate_slug, validate_username])
    first_name  = forms.CharField(label='First Name', max_length=150, validators=[validate_slug])
    last_name = forms.CharField(label='Last Name', max_length=150, validators=[validate_slug])
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
    username = forms.CharField(label='Username', max_length=150, validators=[validate_slug])
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
        datetime.datetime.strptime(value, format).time()
    except Exception:
        raise ValidationError(
            _('%(value)s Wrong time format entered.'),
            code='Wrong time format entered.',
            params={'value': value},
        )

"""Function to check if the email already exists or not."""
def validate_check_in_time(value):
    format = '%H:%M:%S'
    try:
        datetime.datetime.strptime(value, format).time()
    except Exception:
        raise ValidationError(
            _('%(value)s Wrong time format entered.'),
            code='Wrong time format entered.',
            params={'value': value},
        )

class TimeInput(forms.TimeInput):
    input_type = 'time'

from django.utils.timezone import now


class FutureDateInput(forms.DateInput):
    input_type = 'date'

    def get_context(self, name, value, attrs):
        attrs.setdefault('min', now().strftime('%Y-%m-%d'))
        return super().get_context(name, value, attrs)

"""class used for booking a time slot."""
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time', 'check_out_time',
                    'person', 'no_of_rooms']

        widgets = {
                    'check_in_date': FutureDateInput(),
                    'check_in_time': TimeInput(),
                    'check_out_time': TimeInput(),
                }

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        normal_book_date = cleaned_data.get("check_in_date")
        normal_check_in_time = cleaned_data.get("check_in_time")
        normal_check_out_time = cleaned_data.get("check_out_time")
        str_check_in_time = str(normal_check_in_time)
        str_check_out_time = str(normal_check_out_time)
        format = '%H:%M:%S'
        try:
            datetime.datetime.strptime(str_check_in_time, format).time()
            datetime.datetime.strptime(str_check_out_time, format).time()
        except Exception:
            raise ValidationError(
                _('Wrong time entered.'),
                code='Wrong time entered.',
            )

        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (normal_book_date < now.date() or
            (normal_book_date == now.date() and
            normal_check_in_time < now.time())):
            raise ValidationError(
                "You can only book for future.", code='only book for future'
            )
        if normal_check_out_time <= normal_check_in_time:
            raise ValidationError(
                "Check out should be after check in.", code='check out after check in'
            )











class ManageBookingForm(forms.Form):

    room_numbers = forms.CharField(validators=[int_list_validator], required=False, max_length=4000)
    customer_name = forms.CharField(
        max_length=30,
        required=False,
    )
    check_in_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(),
    )
    check_in_time = forms.TimeField(
        required=False,
        widget=TimeInput(),
    )
    check_out_time = forms.TimeField(
        required=False,
        widget=TimeInput(),
    )
    ROOM_CATEGORIES = (
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
        ('King', 'King'),
        ('Queen', 'Queen'),
    )
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=ROOM_CATEGORIES,
    )
    PERSON = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    person = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=PERSON,
        )
    no_of_rooms = forms.IntegerField(
        required=False,
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
        )

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        normal_check_in_time = cleaned_data.get("check_in_time")
        normal_check_out_time = cleaned_data.get("check_out_time")
        #print(cleaned_data.get("check_in_date"))
        str_check_in_time = str(normal_check_in_time)
        str_check_out_time = str(normal_check_out_time)
        format = '%H:%M:%S'
        if str_check_in_time != 'None':
            try:
                datetime.datetime.strptime(str_check_in_time, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if str_check_out_time != 'None':
            try:
                    datetime.datetime.strptime(str_check_out_time, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if normal_check_out_time is not None and normal_check_in_time is not None:
            if normal_check_out_time <= normal_check_in_time:
                raise ValidationError(
                    "Check out should be after check in.", code='check out after check in'
                )


from datetime import time
"""class used for booking a time slot."""
class RoomForm(forms.Form):

    '''room_number = forms.IntegerField(
        required=False,
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )'''

    ROOM_CATEGORIES = (
        #('', ''),
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
        ('King', 'King'),
        ('Queen', 'Queen'),
    )
    '''Regular = forms.BooleanField(required=False)
    Executive = forms.BooleanField(required=False)
    Deluxe = forms.BooleanField(required=False)
    King = forms.BooleanField(required=False)
    Queen = forms.BooleanField(required=False)

    One = forms.BooleanField(required=False)
    Two = forms.BooleanField(required=False)
    Three = forms.BooleanField(required=False)
    Four = forms.BooleanField(required=False)'''

    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=ROOM_CATEGORIES,
    )
    '''category2 = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.Select(choices=ROOM_CATEGORIES),
    )
    category3 = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.Select(choices=ROOM_CATEGORIES),
    )
    category4 = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.Select(choices=ROOM_CATEGORIES),
    )
    category5 = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.Select(choices=ROOM_CATEGORIES),
    )'''

    ROOM_CAPACITY = (
        #('', ''),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    capacity = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=ROOM_CAPACITY,
        )
    '''capacity2 = forms.IntegerField(
        required=False,
        widget=forms.Select(choices=ROOM_CAPACITY),
        )
    capacity3 = forms.IntegerField(
        required=False,
        widget=forms.Select(choices=ROOM_CAPACITY),
        )
    capacity4 = forms.IntegerField(
        required=False,
        widget=forms.Select(choices=ROOM_CAPACITY),
        )'''

    class TimeInput(forms.TimeInput):
        input_type = 'time'
        default=datetime.time()

    available_from = forms.TimeField(
        required=False,
        widget=TimeInput(),
        #initial=time(0)
        )

    available_till = forms.TimeField(
        required=False,
        widget=TimeInput(),
        #initial=time(23,59,59)
        )

    advance = forms.IntegerField(
        required=False,
    )

    '''class Meta:
        model = Room
        fields = ['room_number','category', 'capacity', 'available_from',
                    'available_till', 'advance']

        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

        widgets = {
                    #'room_number': forms.PositiveSmallIntegerField(attrs={'cols': 80, 'rows': 20}),
                    'available_from': TimeInput(),
                    'available_till': TimeInput(),
                }'''

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_till = cleaned_data.get("available_till")
        str_available_from = str(available_from)
        str_available_till = str(available_till)
        format = '%H:%M:%S'
        if str_available_from != 'None':
            try:
                datetime.datetime.strptime(str_available_from, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if str_available_till != 'None':
            try:
                    datetime.datetime.strptime(str_available_till, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if available_till is not None and available_from is not None:
            if available_till <= available_from:
                raise ValidationError(
                    "Available till should be after available from.", code='Available till after available from'
                )


























from datetime import time
"""class used for booking a time slot."""
class RoomForm2(forms.ModelForm):

    room_number = forms.IntegerField(
        required=False,
    )

    ROOM_CATEGORIES = (
        ('', ''),
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
        ('King', 'King'),
        ('Queen', 'Queen'),
    )

    category = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.Select(choices=ROOM_CATEGORIES),
    )

    ROOM_CAPACITY = (
        ('', ''),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    capacity = forms.IntegerField(
        required=False,
        widget=forms.Select(choices=ROOM_CAPACITY),
        )
    class TimeInput(forms.TimeInput):
        input_type = 'time'
        default=datetime.time()

    available_from = forms.TimeField(
        required=False,
        widget=TimeInput(),
        initial=time(0)
        )

    available_till = forms.TimeField(
        required=False,
        widget=TimeInput(),
        initial=time(23,59,59)
        )

    advance = forms.IntegerField(
        required=False,
    )

    class Meta:
        model = Room
        fields = ['room_number','category', 'capacity', 'available_from',
                    'available_till', 'advance']

        '''widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }'''

        """widgets = {
                    #'room_number': forms.PositiveSmallIntegerField(attrs={'cols': 80, 'rows': 20}),
                    'available_from': TimeInput(),
                    'available_till': TimeInput(),
                }"""

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_till = cleaned_data.get("available_till")
        str_available_from = str(available_from)
        str_available_till = str(available_till)
        format = '%H:%M:%S'
        try:
            datetime.datetime.strptime(str_available_from, format).time()
            datetime.datetime.strptime(str_available_till, format).time()
        except Exception:
            raise ValidationError(
                _('Wrong time entered.'),
                code='Wrong time entered.',
            )

        if available_till <= available_from:
            raise ValidationError(
                "Available till should be after available from.", code='Available till after available from'
            )