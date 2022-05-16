from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name='hotel'

urlpatterns = [
	path('admin/', admin.site.urls),
    path('',views.indexView,name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
]
