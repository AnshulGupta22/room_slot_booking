from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
#import datetime
from django.core.validators import int_list_validator, MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.regex_helper import _lazy_re_compile
from datetime import time, date, datetime

from hotel.models import Booking, Room, TimeSlot

slug_re = _lazy_re_compile(r"^[-a-zA-Z0-9_]+\Z")
# A RegexValidator instance that ensures a value consists of only
# letters, numbers, underscores or hyphens.
validate_slug2 = RegexValidator(
    slug_re,
    _("Enter a valid username consisting of letters, numbers, underscores or hyphens."),
    "invalid",
)

"""Function to check if the username already exists or not."""
def validate_username(value):
    new = User.objects.filter(username=value)
    if new.count():
        raise ValidationError(
            _('%(value)s already exists'),
            code='already exists',
            params={'value': value},
        )

"""Function to check if the first name and last name contain only English letters."""
def validate_name(value):
    if not value.isalpha():
        raise ValidationError(
            _('Enter a valid value.This field may contain only English letters. Please do not copy paste here.'),
            code='invalid',
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

"""class for user sign up."""
class CustomerForm(forms.Form):
    username = forms.CharField(label='Desired Username', max_length=150,
                               validators=[validate_slug2, validate_username])
    first_name  = forms.CharField(label='First Name', max_length=150, validators=[validate_name])
    last_name = forms.CharField(label='Last Name', max_length=150, validators=[validate_name])
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

"""class for user sign in."""
class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, validators=[validate_slug2])
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

"""class for editing a user profile."""
class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

"""class for searching rooms."""
class RoomsForm(forms.Form):

    numbers = forms.CharField(validators=[int_list_validator()], required=False, max_length=4000, widget=forms.TextInput(attrs={'class': 'unbold-form'}))

    ROOM_CATEGORIES = (
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
    )

    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'unbold-form'}),
        choices=ROOM_CATEGORIES,
    )

    ROOM_CAPACITIES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    capacities = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'unbold-form'}),
        choices=ROOM_CAPACITIES,
    )

    advance = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'unbold-form'})
    )

    SORT = (
        ('number', 'Numbers: Ascending'),
        ('-number', 'Numbers: Descending'),
        ('capacity', 'Capacities: Ascending'),
        ('-capacity', 'Capacities: Descending'),
        ('advance', 'Advance: Ascending'),
        ('-advance', 'Advance: Descending'),
    )
    sort_by = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'unbold-form'}),
        choices=SORT,
    )
'''
"""class for adding a room."""
class AddRoomForm(forms.ModelForm):
    ROOM_CATEGORIES = (
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
    )

    category = forms.CharField(
        max_length=9,
        widget=forms.RadioSelect(choices=ROOM_CATEGORIES),
    )

    ROOM_CAPACITY = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )

    capacity = forms.CharField(
        max_length=9,
        widget=forms.RadioSelect(choices=ROOM_CAPACITY),
    )
    class Meta:
        model = Room
        fields = ['number', 'category', 'capacity', 'advance']
'''

"""class for adding a room."""
class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'category', 'capacity', 'advance']
        widgets = {'number': forms.NumberInput(attrs={'class': 'unbold-form'}), 'category': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'capacity': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'advance': forms.NumberInput(attrs={'class': 'unbold-form'})}

class NumberInput(forms.NumberInput):
    input_type = 'number'

"""class for editing a room."""
class EditRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['category', 'capacity', 'advance']
        #fields = ['number', 'category', 'capacity', 'advance']
        #widgets = {
        #            'number': NumberInput(attrs={'readonly': True, 'class': 'unbold-form'}), 'category': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'capacity': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'advance': forms.NumberInput(attrs={'class': 'unbold-form'})
        #        }
        widgets = {
                    'category': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'capacity': forms.RadioSelect(attrs={'class': 'unbold-form'}), 'advance': forms.NumberInput(attrs={'class': 'unbold-form'})
                }
class FutureDateInput(forms.DateInput):
    input_type = 'date'

    def get_context(self, name, value, attrs):
        attrs.setdefault('min', now().strftime('%Y-%m-%d'))
        return super().get_context(name, value, attrs)

class TimeInput(forms.TimeInput):
    input_type = 'time'

"""class for searching time slots."""
class SearchTimeSlotsForm(forms.Form):
    # available_from = forms.TimeField(required=False, widget=TimeInput(attrs={'class': 'unbold-form'}), initial=time(0))
    # available_till = forms.TimeField(required=False, widget=TimeInput(attrs={'class': 'unbold-form'}), initial=time(23,59,59))

    # available_from = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}), initial=time(0))
    # available_till = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}), initial=time(23,59))

    date = forms.DateField(widget=FutureDateInput(attrs={'class': 'unbold-form'}), required=False, initial=date.today())

    available_from = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}), required=False)
    available_till = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}), required=False)

    STATUS = (
        (None, 'Any'),
        ('Vacant', 'Vacant'),
        ('Booked', 'Booked'),
    )
    occupancy = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'unbold-form'}),
        choices=STATUS,
    )

    '''occupancies = forms.ChoiceField(
        required=False,
        choices=STATUS,
    )'''

    SORT = (
        ('available_from', 'Ascending'),
        ('-available_from', 'Descending'),
    )
    sort_by = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'unbold-form'}),
        choices=SORT,
    )

    """Function to ensure that booking is done for future and check out is after check in"""
    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_till = cleaned_data.get("available_till")

        if (available_from is not None and available_till is None) or (available_from is None and available_till is not None):
            # Here we're raising a ValidationError that refers to a specific
            # field so the error is better pointed out to the user.
            raise ValidationError(
                _("You can either fill both 'Available from' and 'Available till' or choose not to fill both of them."),
                code='invalid'
            )

        str_available_from = str(available_from)
        str_available_till = str(available_till)
        format = '%H:%M:%S'
        # if str_available_from != 'None':
        #     try:
        #         datetime.datetime.strptime(str_available_from, format).time()
        #     except Exception:
        #         raise ValidationError(
        #             _('Wrong time entered.'),
        #             code='Wrong time entered.',
        #         )
        # if str_available_till != 'None':
        #     try:
        #         datetime.datetime.strptime(str_available_till, format).time()
        #     except Exception:
        #         raise ValidationError(
        #             _('Wrong time entered.'),
        #             code='Wrong time entered.',
        #         )
        if available_from is not None:
            try:
                datetime.strptime(str_available_from, format).time()
                datetime.strptime(str_available_till, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
            if available_till <= available_from:
                raise ValidationError(
                    "Available till should be after available from.", code='Available till after available from'
                )

class AddTimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['available_from', 'available_till']
        widgets = {
                    #'number': PositiveSmallIntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], attrs={'readonly': True}),
                    #'available_from': TimeInput(attrs={'readonly': True}),
                    'available_from': TimeInput(attrs={'class': 'unbold-form'}),
                    'available_till': TimeInput(attrs={'class': 'unbold-form'})
                }

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
                datetime.strptime(str_available_from, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if str_available_till != 'None':
            try:
                    datetime.strptime(str_available_till, format).time()
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



"""class used for booking."""
# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['check_in_date', 'check_in_time', 'check_out_time',
#                     'person', 'no_of_rooms']

#         widgets = {
#                     'check_in_date': FutureDateInput(),
#                     'check_in_time': TimeInput(),
#                     'check_out_time': TimeInput(),
#                 }

#     """Function to ensure that booking is done for future and check out is after check in"""
#     def clean(self):
#         cleaned_data = super().clean()
#         normal_book_date = cleaned_data.get("check_in_date")
#         normal_check_in_time = cleaned_data.get("check_in_time")
#         normal_check_out_time = cleaned_data.get("check_out_time")
#         str_check_in_time = str(normal_check_in_time)
#         str_check_out_time = str(normal_check_out_time)
#         format = '%H:%M:%S'
#         try:
#             datetime.datetime.strptime(str_check_in_time, format).time()
#             datetime.datetime.strptime(str_check_out_time, format).time()
#         except Exception:
#             raise ValidationError(
#                 _('Wrong time entered.'),
#                 code='Wrong time entered.',
#             )

#         # now is the date and time on which the user is booking.
#         now = timezone.now()
#         if (normal_book_date < now.date() or
#             (normal_book_date == now.date() and
#             normal_check_in_time < now.time())):
#             raise ValidationError(
#                 "You can only book for future.", code='only book for future'
#             )
#         if normal_check_out_time <= normal_check_in_time:
#             raise ValidationError(
#                 "Check out should be after check in.", code='check out after check in'
#             )

"""class used for booking."""
class BookingForm(forms.Form):

    check_in_date = forms.DateField(widget=FutureDateInput(attrs={'class': 'unbold-form'}), initial=date.today())
    check_in_time = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}))
    check_out_time = forms.TimeField(widget=TimeInput(attrs={'class': 'unbold-form'}))
    PERSONS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    person = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'unbold-form'}),
        choices=PERSONS, initial=1
    )
    # no_of_rooms =  forms.IntegerField(
    #     validators=[MaxValueValidator(100), MinValueValidator(1)], initial=1
    #     )


        # widgets = {
        #             'check_in_date': FutureDateInput(),
        #             'check_in_time': TimeInput(),
        #             'check_out_time': TimeInput(),
        #         }

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
            datetime.strptime(str_check_in_time, format).time()
            datetime.strptime(str_check_out_time, format).time()
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



















"""Function to convert string to date."""
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    try:
        datetime.strptime(date_time, format).date()
    except Exception:
        raise ValidationError(
                "Wrong date format entered.", code='Wrong date format'
            )

"""Function to convert string to time."""
def convert_to_time(value):
    format = '%H:%M:%S'
    try:
        datetime.strptime(value, format).time()
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
        datetime.strptime(value, format).time()
    except Exception:
        raise ValidationError(
            _('%(value)s Wrong time format entered.'),
            code='Wrong time format entered.',
            params={'value': value},
        )



from django.utils.timezone import now






class ManageBookingForm(forms.Form):

    room_numbers = forms.CharField(validators=[int_list_validator()], required=False, max_length=4000)
    customer_name = forms.CharField(
        max_length=150,
        required=False,
        validators=[validate_slug2]
    )
    check_in_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(),
    )
    check_in_time = forms.TimeField(
        required=False,
        widget=TimeInput()
    )
    check_out_time = forms.TimeField(
        required=False,
        widget=TimeInput()
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
        str_check_in_time = str(normal_check_in_time)
        str_check_out_time = str(normal_check_out_time)
        format = '%H:%M:%S'
        if str_check_in_time != 'None':
            try:
                datetime.strptime(str_check_in_time, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if str_check_out_time != 'None':
            try:
                    datetime.strptime(str_check_out_time, format).time()
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

















'''class SearchTimeSlotsForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['available_from', 'available_till']
        widgets = {
                    #'number': PositiveSmallIntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], attrs={'readonly': True}),
                    'available_from': TimeInput(attrs={'required': False}),
                    'available_till': TimeInput(attrs={'required': False}),
                }'''

    

class ManageViewTimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['room', 'available_from', 'available_till']
        widgets = {
                    'room': forms.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)]),
                    'available_from': TimeInput(attrs={'required': False}),
                    'available_till': TimeInput(attrs={'required': False}),
                }

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
                datetime.strptime(str_available_from, format).time()
            except Exception:
                raise ValidationError(
                    _('Wrong time entered.'),
                    code='Wrong time entered.',
                )
        if str_available_till != 'None':
            try:
                    datetime.strptime(str_available_till, format).time()
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




















#from datetime import time
"""class used for booking a time slot."""
class RoomForm2(forms.ModelForm):

    number = forms.IntegerField(
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
        default=time()

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
        fields = ['number','category', 'capacity', 'available_from',
                    'available_till', 'advance']

        '''widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }'''

        """widgets = {
                    #'number': forms.PositiveSmallIntegerField(attrs={'cols': 80, 'rows': 20}),
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
            datetime.strptime(str_available_from, format).time()
            datetime.strptime(str_available_till, format).time()
        except Exception:
            raise ValidationError(
                _('Wrong time entered.'),
                code='Wrong time entered.',
            )

        if available_till <= available_from:
            raise ValidationError(
                "Available till should be after available from.", code='Available till after available from'
            )