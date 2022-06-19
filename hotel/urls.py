from django.urls import path,include
from . import views
#from django.contrib.auth.views import LoginView,LogoutView

app_name='hotel'

urlpatterns = [
    #path('',views.indexView,name="home"),
    #path('dashboard/',views.dashboardView,name="dashboard"),
    #path('login/',LoginView.as_view(),name="login_url"),
    path('home/', views.home, name="home"),
    path('book/', views.booking, name="book"),
    path('signup/', views.sign_up, name="signup"),
    path('signup/welcome/', views.sign_in),
    path('signin/', views.sign_in, name="signin"),
    path('signin/signedin/', views.booking),
    path('logout/', views.logout_view, name="logout"),
    path('yac/', views.yac, name="yac"),
    #path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
]
