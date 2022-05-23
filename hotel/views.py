'''
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html', {'form': form})
'''    
from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from hotel.forms import HotelForm, SigninForm
from django.http import HttpResponse

# Create your views here.
'''
def indexView(request):
    return render(request,'index.html')
@login_required()

def dashboardView(request):
    return render(request,'dashboard.html')
'''

def home(request):
    return render(request,'home.html')
    
def sign_up(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid() and request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.create_user(request.POST['username'],  request.POST['email'], request.POST['password'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
		        #form.save()
                return redirect('welcome/')
            except:
       	        return HttpResponse("Username already exist")
        else:
            context = {'form': form}
            return render(request, 'signup.html', context)
    context = {'form': HotelForm()}
    return render(request, 'signup.html', context)

def sign_in(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('signedin/')
            else:
                return HttpResponse("Invalid Credentials")
        else:
            context = {'form': form}
            return render(request, 'signin.html', context)
    context = {'form': SigninForm()}
    return render(request, 'signin.html', context)

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request,'logout.html')
'''    
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
'''

def welcome(request):
    return render(request,'welcome.html')
    
def signedin(request):
    return render(request,'signedin.html')
