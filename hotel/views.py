from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from hotel.forms import HotelForm, SigninForm, AvailabilityForm
from django.http import HttpResponse
from . models import Customer, Room, Hotel
import datetime

# Create your views here.

username = ''

# Function to convert string to date
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    datetime_str = datetime.datetime.strptime(date_time, format).date()
    return datetime_str

# Function to convert string to time
def convert_to_time(date_time):
    format = '%H:%M'
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
    #return redirect('signin/')
    
def check_availability(category, book_date, check_in, check_out, now, capacity):
    #check_in = book_from.time()
    room_list = Room.objects.filter(category = category, available_from__lt = check_in,  available_till__gt =  check_out)
    for room in room_list:
        booking_list = Customer.objects.filter(book_from_time__lt = check_out,  book_till_time__gt = check_in, book_from_date = book_date)
        if not booking_list:
            booked_number = room.room_number    
            nextD = now + datetime.timedelta(days=room.advance)
            
            
            if(book_date <= nextD.date()):
                #nextD = now + datetime.timedelta(days=5)
                #avb = Room.objects.filter(available_from__lt = check_in,  available_till__gt =  check_out, room_number = booked_number)
                #if avb:
                time_slot = Customer(user = username, book_from_date = book_date, book_from_time = check_in, book_till_time = check_out, room_number = booked_number, category = category, capacity = capacity)
                time_slot.save()
                return True
    return False
    
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            now = datetime.datetime.now()
            #print(now)
            #nextD = now + datetime.timedelta(days=5)
            #print(nextD)
            book_from_date = request.POST['book_from_date']
            book_from_time = request.POST['book_from_time']
            book_till_time = request.POST['book_till_time']
            category = request.POST['category']
            capacity = request.POST['capacity']
            converted_book_from_date = convert_to_date(book_from_date)
            converted_book_from_time = convert_to_time(book_from_time)
            converted_book_till_time = convert_to_time(book_till_time)
            if(check_availability(category, converted_book_from_date, converted_book_from_time, converted_book_till_time, now, capacity)):
                return HttpResponse("Booked")
            return HttpResponse("Not Booked")
        else:
            context = {'form': AvailabilityForm()}
            return render(request, 'book.html', context)
    context = {'form': AvailabilityForm()}
    return render(request, 'book.html', context)
