from django.urls import path
from . import views
#from django.contrib.auth.views import LoginView,LogoutView

app_name='hotel'

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
    path('future/', views.future, name='future'),
    path('future/<int:booking_id>/', views.future, name='delete_booking'),
    path('all_bookings/', views.all_bookings, name='all_bookings'),
    #path('logout/',LogoutView.as_view(next_page='dashboard'),name='logout'),
    #path('',views.indexView,name='home'),
    #path('login/',LoginView.as_view(),name='login_url'),
]
