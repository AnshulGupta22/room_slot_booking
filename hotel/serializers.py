from rest_framework import serializers
from . models import Room, Customer, Booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'category', 'capacity', 'available_from', 
        'available_till', 'advance']
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['desired_username', 'first_name', 'last_name', 'email']
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        #fields = ['id', 'customer_name', 'book_from_date', 'book_from_time', 
        #'book_till_time',  'room_number', 'category', 'capacity']
        fields = ['book_from_date', 'book_from_time', 
        'book_till_time', 'capacity']
        
class BookingSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer_name', 'book_from_date', 'book_from_time', 
        'book_till_time',  'room_number', 'category', 'capacity']
