from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

"""class used when a user sign up."""
class Customer(models.Model):
    desired_username = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

"""class used when a user sign up using API."""
class CustomerAPI(models.Model):
    desired_username = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=120)
    confirm_password = models.CharField(max_length=120)

"""class used when a user sign in."""
class SignIn(models.Model):
    username = models.CharField(max_length=30)

"""class used to represent a room."""
class Room(models.Model):
    room_number =  models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)],
        primary_key=True
        )
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    ROOM_CAPACITY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    capacity = models.CharField(max_length=3, choices=ROOM_CAPACITY)
    available_from = models.TimeField()
    available_till = models.TimeField()
    advance = models.PositiveSmallIntegerField()

"""class used when a user books a room slot."""
class Booking(models.Model):
    customer_name = models.CharField(max_length=30)
    book_from_date = models.DateField()
    book_from_time = models.TimeField()
    book_till_time = models.TimeField()
    room_number =  models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
        )
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    ROOM_CAPACITY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    capacity = models.CharField(max_length=3, choices=ROOM_CAPACITY)

