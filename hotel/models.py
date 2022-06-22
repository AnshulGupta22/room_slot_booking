from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
#import datetime
from datetime import date
# Create your models here.

class Hotel(models.Model):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

class Room(models.Model):
    #rooms_available = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    room_number =  models.PositiveSmallIntegerField(validators=[MaxValueValidator(1000),MinValueValidator(1)])
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    room_capacity = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    capacity = models.CharField(max_length=3, choices=room_capacity)
    #available_from = models.DateTimeField()
    #available_till = models.DateTimeField()
    available_from = models.TimeField()
    available_till = models.TimeField()
    advance = models.PositiveSmallIntegerField()
    
    '''def __str__(self):
        return self.room_number, self.category, self.capacity, self.available_from, self.available_till, self.advance'''
    #room_number =  models.PositiveSmallIntegerField()
'''
class Room(models.Model):
	room = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(10),MinValueValidator(1)])
'''
class Customer(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    user = models.CharField(max_length=30)
    book_from_date = models.DateField()
    #book_from = models.TimeField()
    book_from_time = models.TimeField()
    book_till_time = models.TimeField()
    room_number =  models.PositiveSmallIntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)])
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    room_capacity = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    capacity = models.CharField(max_length=3, choices=room_capacity)
    '''
    def __str__(self):
        return self.user, self.book_from_date, self.book_from_time, self.book_till_time, self.room_number, self.category, self.capacity'''
    
'''    
class Booking(models.Model):
    #user = models.CharField(max_length=30)
    book_from = models.DateTimeField()
    book_till = models.DateTimeField()
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)'''
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
'''
