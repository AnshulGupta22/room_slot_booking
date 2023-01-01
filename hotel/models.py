from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.core.validators import validate_comma_separated_integer_list, int_list_validator
from django.core.validators import int_list_validator

# Create your models here.

"""class for representing a room."""
class Room(models.Model):
    class Meta:
      ordering = ['number']
    number =  models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)],
        primary_key=True
        )
    CATEGORIES = (
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
    )
    category = models.CharField(max_length=9, choices=CATEGORIES, default='Regular')
    CAPACITY = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    capacity = models.PositiveSmallIntegerField(
        choices=CAPACITY, default=2
        )
    advance = models.PositiveSmallIntegerField(default=10)
    manager = models.CharField(max_length=30)

    def __str__(self):
        return f'Room number: {self.number}, category: {self.category}, capacity: {self.capacity}, advance: {self.advance}, room manager: {self.manager}'

class TimeSlot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    available_from = models.TimeField()
    available_till = models.TimeField()
    STATUS = (
        ('Vacant', 'Vacant'),
        ('Booked', 'Booked'),
    )
    occupancy = models.CharField(max_length=6, choices=STATUS, default='Vacant')
    #booked = models.BooleanField(default=False)

    def __str__(self):
        return f'Room: {self.room}, from: {self.available_from}, till: {self.available_till}, occupancy: {self.occupancy}'

"""class used when a user books a room slot."""
class Booking(models.Model):
    #class Meta:
    #  ordering = ['-check_in_date', 'check_in_time']
    customer_name = models.CharField(max_length=150)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    '''number =  models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)], unique=True
        )'''
    room_numbers = models.CharField(validators=[int_list_validator(' ,')], max_length=4000)
    CATEGORIES = (
        ('Regular', 'Regular'),
        ('Executive', 'Executive'),
        ('Deluxe', 'Deluxe'),
        ('King', 'King'),
        ('Queen', 'Queen'),
    )
    category = models.CharField(max_length=9, choices=CATEGORIES)
    PERSON = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    person = models.PositiveSmallIntegerField(choices=PERSON, default=1)
    no_of_rooms = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1
        )
    room_managers = models.CharField(validators=[int_list_validator(' ,')], max_length=4000)
    def __str__(self):
        return f'Customer name: {self.customer_name}; check in date: {self.check_in_date}; check in time: {self.check_in_time}; check out time: {self.check_out_time}; room number: {self.room_numbers}; category: {self.category}; number of person: {self.person}'
