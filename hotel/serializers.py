from rest_framework import serializers
from . models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'category', 'capacity', 'available_from', 
        'available_till', 'advance']
