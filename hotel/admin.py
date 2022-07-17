from django.contrib import admin

from hotel.models import Customer, Room, Booking

# Register your models here.

admin.site.register(Room)
admin.site.register(Booking)
