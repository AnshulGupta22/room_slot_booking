from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'hotel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('book/', views.booking, name='book'),
    path('logout/', views.logout_view, name='logout'),
    path('yac/', views.yac, name='yac'),
    path('nac/', views.nac, name='nac'),
    path('deluxe/', views.deluxe, name='deluxe'),
    path('king/', views.king, name='king'),
    path('queen/', views.queen, name='queen'),
    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('all_bookings/<int:booking_id>/', views.all_bookings, name='delete_booking'),
    path('rooms/', views.room_list),
    path('rooms/<int:pk>/', views.room_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
