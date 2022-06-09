from django.contrib import admin

# Register your models here.

#from hotel.models import Hotel
#admin.site.register(Hotel)

from hotel.models import RoomAvailable, Booking, Room
admin.site.register(RoomAvailable)
admin.site.register(Booking)
admin.site.register(Room)
