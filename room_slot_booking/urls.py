"""room_slot_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
#from django.contrib.auth import views as auth_views
#from hotel.forms import SigninForm, LoginForm

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel/',include('hotel.urls', namespace='hotel')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #path('api-auth/', include('rest_framework.urls')),
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('signin/', auth_views.LoginView, {'template_name': 'signin.html', 'authentication_form': SigninForm}, name='signin'),
    #path('signin/', auth_views.LoginView.as_view(template_name='signin.html', authentication_form=LoginForm), name='signin'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/signin'), name='logout'),
]
