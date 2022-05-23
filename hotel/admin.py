from django.contrib import admin

# Register your models here.

#from hotel.models import Hotel
#admin.site.register(Hotel)

from hotel.models import Room, TimeSlot
admin.site.register(Room)
admin.site.register(TimeSlot)
