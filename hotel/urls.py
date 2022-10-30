from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'hotel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('book/', views.booking, name='book'),
    path('logout/', views.logout_view, name='logout'),
    path('regular/', views.regular, name='regular'),
    path('executive/', views.executive, name='executive'),
    path('deluxe/', views.deluxe, name='deluxe'),
    path('king/', views.king, name='king'),
    path('queen/', views.queen, name='queen'),
    path('booked/', views.booked, name='booked'),
    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('all_bookings/<int:pk>/', views.all_bookings, name='delete_booking'),
    path('rooms/', views.room_list),
    path('rooms/<int:pk>/', views.room_detail),
    path('users/', views.user_list),
    path('bookings/', views.booking_list),
    path('bookings/<int:pk>/', views.booking_detail),
    path('bookings/<category>/', views.booking_category),
]

urlpatterns = format_suffix_patterns(urlpatterns)
