from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from hotel.forms import HotelForm, SigninForm, BookForm, AvailabilityForm
from django.http import HttpResponse
from . models import Booking, Room, RoomAvailable
import datetime

# Create your views here.

username = ''

# Function to convert string to datetime
def convert(date_time):
    #format = '%I:%M' # The format
    format = '%Y-%m-%d %H:%M'
    datetime_str = datetime.datetime.strptime(date_time, format).time()
   
    return datetime_str

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
            global username
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
    
def welcome(request):
    return render(request,'welcome.html')
    
def signedin(request):
    return HttpResponse("Welcome user")
    
def check_availability(category, check_in, check_out):
    room_list = Room.objects.filter(category = category)
    for room in room_list:
        booking_list = Room.objects.filter(book_from__lt = check_out,  book_till__gt =  check_in)
        if not booking_list:
            booked_number = room.room_number
            avb = RoomAvailable.objects.filter(available_from__lt = check_in,  available_till__gt =  check_out, room_number = booked_number)
            if avb:
                time_slot = Room(user = username, book_from = check_in, book_till = check_out, room_number = booked_number, category = category)
            time_slot.save()
            return True
    return False
    
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            now = datetime.datetime.now()
            print(now)
            book_from = request.POST['book_from']
            book_till = request.POST['book_till']
            category = request.POST['category']
            converted_start_time = convert(book_from)
            converted_end_time = convert(book_till)
            if(check_availability(category, book_from, book_till)):
                return HttpResponse("Booked")
                new_slot = Room.objects.get(category = category)
                new_slot.user = username
                new_slot.book_from = username
                new_slot.book_till = username
                new_slot.user = username
                new_slot.save()
                return HttpResponse("Booked")
            return HttpResponse("Not Booked")
        else:
            context = {'form': AvailabilityForm()}
            return render(request, 'book.html', context)
    context = {'form': AvailabilityForm()}
    return render(request, 'book.html', context)
