from django.contrib import admin

# Register your models here.

#from hotel.models import Hotel
#admin.site.register(Hotel)

from hotel.models import TimeSlot, RoomAvailable
admin.site.register(RoomAvailable)
#admin.site.register(Room)
admin.site.register(TimeSlot)
