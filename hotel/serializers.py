from rest_framework import serializers
from . models import Room, Booking
from django.contrib.auth.models import User
from django.utils import timezone

"""class for rooms."""
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'category', 'capacity', 'available_from',
                    'available_till', 'advance']

"""class for users."""
"""class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['desired_username', 'first_name', 'last_name', 'email']"""

"""class to register users."""
'''class CustomerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAPI
        fields = ['desired_username', 'first_name', 'last_name', 'email',
                    'password',  'confirm_password']'''

""""""""""""""""""""""""""""""""""""""""""

class CustomerAPISerializer(serializers.Serializer):
    desired_username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    your_email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    retype_password = serializers.CharField(min_length=8)

    def validate(self, data):
        """
        Check if password and retyped password match or not.
        """
        if data['password'] != data['retype_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def validate_desired_username(self, value):
        """
        Check if the username already exists or not.
        """
        new = User.objects.filter(username = value)
        if new.count():
            raise serializers.ValidationError(f'{value} already exists')
        return value

    def validate_your_email(self, value):
        """
        Check if the email already exists or not.
        """
        new = User.objects.filter(email = value)
        if new.count():
            raise serializers.ValidationError(f'{value} already exists')
        return value

""""""""""""""""""""""""""""""""""""""""""

"""class for bookings for use by admin."""
class BookingSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer_name', 'check_in_date', 'check_in_time',
                    'check_out_time',  'room_number', 'category', 'person', 'no_of_rooms']

    def validate(self, data):
        """
        Function to ensure that booking is done for future.
        """
        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (data['check_in_date']  < now.date() or (data['check_in_date'] == now.date() and
            data['check_in_time'] < now.time())):
            raise serializers.ValidationError("You can only book for future.")
        return data

"""class for bookings without id for use by admin."""
class BookingSerializerAdminWithoutid(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer_name', 'check_in_date', 'check_in_time',
                    'check_out_time',  'room_number', 'category', 'person', 'no_of_rooms']

    def validate(self, data):
        """
        Function to ensure that booking is done for future.
        """
        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (data['check_in_date']  < now.date() or (data['check_in_date'] == now.date() and
            data['check_in_time'] < now.time())):
            raise serializers.ValidationError("You can only book for future.")
        return data

"""class to get bookings."""
class BookingSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'check_in_date', 'check_in_time',
                    'check_out_time', 'category', 'person', 'no_of_rooms']

    def validate(self, data):
        """
        Function to ensure that booking is done for future.
        """
        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (data['check_in_date']  < now.date() or (data['check_in_date'] == now.date() and
            data['check_in_time'] < now.time())):
            raise serializers.ValidationError("You can only book for future.")
        if data['check_out_time'] <= data['check_in_time']:
            raise serializers.ValidationError("Check out should be after check in.")
        return data

"""class to book booking."""
class BookingSerializerBook(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time',
                    'check_out_time', 'person', 'no_of_rooms']

    def validate(self, data):
        """
        Function to ensure that booking is done for future.
        """
        # now is the date and time on which the user is booking.
        now = timezone.now()
        if (data['check_in_date']  < now.date() or (data['check_in_date'] == now.date() and
            data['check_in_time'] < now.time())):
            raise serializers.ValidationError("You can only book for future.")
        return data