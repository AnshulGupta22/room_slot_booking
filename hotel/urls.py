from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'hotel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('room_manager/', views.room_manager, name='room_manager'),
    path('rooms/', views.rooms, name='rooms'),
    path('manage_time_slots/', views.manage_time_slots, name='manage_time_slots'),
    path('view_time_slots/<int:room_number>/', views.view_time_slots, name='view_time_slots'),
    path('add_time_slots/<int:room_number>/', views.add_time_slots, name='add_time_slots'),
    path('edit_time_slots/<int:pk>/', views.edit_time_slots, name='edit_time_slots'),
    path('delete_time_slot/<int:pk>/', views.delete_time_slot, name='delete_time_slot'),
    path('add_room/', views.add_room, name='add_room'),
    path('edit_rooms/<int:room_number>/', views.edit_rooms, name='edit_rooms'),
    path('delete_rooms/<int:room_number>/', views.delete_rooms, name='delete_rooms'),
    path('book/', views.booking, name='book'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('regular/', views.regular, name='regular'),
    path('executive/', views.executive, name='executive'),
    path('deluxe/', views.deluxe, name='deluxe'),
    path('king/', views.king, name='king'),
    path('queen/', views.queen, name='queen'),
    path('booked_regular/', views.booked_regular, name='booked_regular'),
    path('booked_executive/', views.booked_executive, name='booked_executive'),
    path('booked_deluxe/', views.booked_deluxe, name='booked_deluxe'),
    path('booked_king/', views.booked_king, name='booked_king'),
    path('booked_queen/', views.booked_queen, name='booked_queen'),
    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('all_bookings/<int:pk>/', views.all_bookings, name='delete_booking'),
    #path('rooms/', views.room_list),
    #path('rooms/<int:pk>/', views.room_detail),
    path('users/', views.user_list),
    path('bookings/', views.booking_list),
    path('bookings/<int:pk>/', views.booking_detail),
    path('bookings/<category>/', views.booking_category),
    path('profile_view/', views.profile_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)
