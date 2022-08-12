from rest_framework import serializers
from . models import Room, Customer, Booking, CustomerAPI

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'category', 'capacity', 'available_from', 
                    'available_till', 'advance']
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['desired_username', 'first_name', 'last_name', 'email']
        
class CustomerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAPI
        fields = ['desired_username', 'first_name', 'last_name', 'email',
                    'password',  'confirm_password']
     
class BookingSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer_name', 'book_from_date', 'book_from_time', 
                    'book_till_time',  'room_number', 'category', 'capacity']
     
class BookingSerializerAdminWithoutid(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer_name', 'book_from_date', 'book_from_time', 
                    'book_till_time',  'room_number', 'category', 'capacity']   
class BookingSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'book_from_date', 'book_from_time', 
                    'book_till_time', 'category', 'capacity']
        
class BookingSerializerBook(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['book_from_date', 'book_from_time', 
                    'book_till_time', 'capacity']
        
