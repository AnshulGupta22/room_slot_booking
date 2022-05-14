from django.urls import path
from . import views

app_name='hotel'

urlpatterns = [
	path('index/', views.index, name='index'),
    path('count_rooms/', views.count_rooms, name='count_rooms'),
#	path('audio/video/', views.video),
#	path('audio/video/download/', views.download),
]
