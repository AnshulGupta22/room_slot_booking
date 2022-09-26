from rest_framework import serializers
from . models import Room, Customer, Booking, CustomerAPI

"""class for rooms."""
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'category', 'capacity', 'available_from',
                    'available_till', 'advance']

"""class for users."""
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['desired_username', 'first_name', 'last_name', 'email']

"""class to register users."""
class CustomerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAPI
        fields = ['desired_username', 'first_name', 'last_name', 'email',
                    'password',  'confirm_password']

"""class for bookings for use by admin."""
class BookingSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer_name', 'check_in_date', 'check_in_time',
                    'check_out_time',  'room_number', 'category', 'person']

"""class for bookings without id for use by admin."""
class BookingSerializerAdminWithoutid(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer_name', 'check_in_date', 'check_in_time',
                    'check_out_time',  'room_number', 'category', 'person']

"""class to get bookings."""
class BookingSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'check_in_date', 'check_in_time',
                    'check_out_time', 'category', 'person']

"""class to book booking."""
class BookingSerializerBook(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_in_time',
                    'check_out_time', 'person']

