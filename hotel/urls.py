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
    path('rooms/', views.rooms, name='rooms'),
    path('add_room/', views.add_room, name='add_room'),
    path('edit_room/<int:number>/', views.edit_room, name='edit_room'),
    path('delete_room/<int:number>/', views.delete_room, name='delete_room'),
    path('time_slots/<int:number>/', views.time_slots, name='time_slots'),
    path('add_time_slot/<int:number>/', views.add_time_slot, name='add_time_slot'),
    path('edit_time_slot/<int:pk>/', views.edit_time_slot, name='edit_time_slot'),
    path('delete_time_slot/<int:pk>/', views.delete_time_slot, name='delete_time_slot'),
    path('manager_bookings/', views.manager_bookings, name='manager_bookings'),
    path('manager_delete_booking/<int:pk>/', views.manager_delete_booking, name='manager_delete_booking'),
    path('book/', views.booking, name='book'),
    path('regular/', views.regular, name='regular'),
    path('executive/', views.executive, name='executive'),
    path('deluxe/', views.deluxe, name='deluxe'),
    # path('king/', views.king, name='king'),
    # path('queen/', views.queen, name='queen'),
    path('booked_regular/', views.booked_regular, name='booked_regular'),
    path('booked_executive/', views.booked_executive, name='booked_executive'),
    path('booked_deluxe/', views.booked_deluxe, name='booked_deluxe'),
    # path('booked_king/', views.booked_king, name='booked_king'),
    # path('booked_queen/', views.booked_queen, name='booked_queen'),
    path('customer_bookings/', views.customer_bookings, name='customer_bookings'),
    path('customer_bookings/<int:pk>/', views.customer_bookings, name='delete_booking'),
    #path('rooms/', views.room_list),
    #path('rooms/<int:pk>/', views.room_detail),
    path('users/', views.user_list),
    # path('bookings/', views.booking_list),
    # path('bookings/<int:pk>/', views.booking_detail),
    # path('bookings/<category>/', views.booking_category),
    path('profile_view/', views.profile_view),
    #path('manage_time_slots/', views.manage_time_slots, name='manage_time_slots'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
