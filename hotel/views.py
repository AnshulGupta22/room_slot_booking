'''
from django.shortcuts import render
from django.http import HttpResponse
from .models import Hotel

# Create your views here.

def index(request):
    return HttpResponse("Hello World")
    
def count_rooms(request):
    #count_rooms = Hotel.objects.count()
    #return HttpResponse(count_rooms)
    count_rooms = Hotel.objects.all()
    context = {'hot': count_rooms}
    return render(request, 'qwert.html', context)
'''

from django.shortcuts import render,redirect
from django.contrib.auth.models import Hotel
from django.contrib import auth

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                Hotel.objects.get(username = request.POST['username'])
                return render (request,'accounts/signup.html', {'error':'Username is already taken!'})
            except Hotel.DoesNotExist:
                user = Hotel.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'accounts/signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'accounts/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')


