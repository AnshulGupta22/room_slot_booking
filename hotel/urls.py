from django.urls import path,include
from . import views
from django.contrib import admin

app_name='hotel'

urlpatterns = [
	#path('index/', views.index, name='index'),
    #path('count_rooms/', views.count_rooms, name='count_rooms'),
    path('signup/', views.signup, name='signup'),
#	path('audio/video/', views.video),
#	path('audio/video/download/', views.download),
]
