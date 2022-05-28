from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Hotel(models.Model):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

class RoomAvailable(models.Model):
    rooms_available = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
'''
class Room(models.Model):
	room = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(10),MinValueValidator(1)])
'''
class Book(models.Model):
    room_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    book_from = models.TimeField()
    book_till = models.TimeField()
    
class TimeSlot(models.Model):
    #room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_number = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(10),MinValueValidator(1)])
    room_available_from1 = models.TimeField(blank=True, default=None, null=True)
    room_available_till1 = models.TimeField(blank=True, default=None, null=True)
    room_available_from2 = models.TimeField(blank=True, default=None, null=True)
    room_available_till2 = models.TimeField(blank=True, default=None, null=True)
    room_available_from3 = models.TimeField(blank=True, default=None, null=True)
    room_available_till3 = models.TimeField(blank=True, default=None, null=True)
    room_available_from4 = models.TimeField(blank=True, default=None, null=True)
    room_available_till4 = models.TimeField(blank=True, default=None, null=True)
    room_available_from5 = models.TimeField(blank=True, default=None, null=True)
    room_available_till5 = models.TimeField(blank=True, default=None, null=True)
    room_available_from6 = models.TimeField(blank=True, default=None, null=True)
    room_available_till6 = models.TimeField(blank=True, default=None, null=True)

