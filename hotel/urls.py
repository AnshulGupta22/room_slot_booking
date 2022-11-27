from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'hotel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('book/', views.booking, name='book'),
    path('manage/', views.manage, name='manage'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('add_rooms/', views.add_rooms, name='add_rooms'),
    path('add_rooms/<int:room_number>/', views.add_rooms, name='edit_rooms'),
    path('delete_rooms/<int:room_number>/', views.delete_rooms, name='delete_rooms'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('logout/', views.logout_view, name='logout'),
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
    path('rooms/', views.room_list),
    path('rooms/<int:pk>/', views.room_detail),
    path('users/', views.user_list),
    path('bookings/', views.booking_list),
    path('bookings/<int:pk>/', views.booking_detail),
    path('bookings/<category>/', views.booking_category),
    path('profile_view/', views.profile_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)
