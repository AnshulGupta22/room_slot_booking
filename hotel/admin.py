from django.contrib import admin

from hotel.models import Room, Booking, TimeSlot

# Register your models here.

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(TimeSlot)
