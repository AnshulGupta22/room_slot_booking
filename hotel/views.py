from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from hotel.forms import HotelForm, SigninForm, AvailabilityForm
from django.http import HttpResponse
from . models import Customer, Room, Hotel
import datetime
from django.db.models import Q

# Create your views here.

username = ''
registered = 0
converted_book_from_date = datetime.date(1996, 12, 11)
converted_book_from_time = datetime.time(13, 24, 56)
converted_book_till_time = datetime.time(13, 24, 56)
capacity = 1
dict1 = dict()

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
                global username
                username = request.POST['username']
                global registered
                registered = 1
                return redirect('../book/')
            except:
       	        return HttpResponse("Username already exist")
        else:
            context = {'form': form}
            return render(request, 'signup.html', context)
    context = {'form': HotelForm()}
    return render(request, 'signup.html', context)

def sign_in(request):
    global registered
    if registered == 0:
        if request.method == 'POST':
            form = SigninForm(request.POST)
            if form.is_valid():
                global username
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('../book/')
                else:
                    return HttpResponse("Invalid Credentials")
            else:
                context = {'form': form}
                return render(request, 'signin.html', context)
        context = {'form': SigninForm()}
        return render(request, 'signin.html', context)
    else:
        return redirect('../book/')

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    #return render(request,'logout.html')
    return redirect('../signin/')
    
def check_availability(category, book_date, check_in, check_out, now, capacity):
    global dict1
    room_list = Room.objects.filter(available_from__lte = check_in, available_till__gte =  check_out, capacity__gte = capacity)
    #print("vetgtegv")
    #print(room_list)
    #print("tgevd")
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance) 
        if(book_date <= max_book.date()):
            #This logic works for a particular room
            taken = Customer.objects.filter(Q(Q(book_from_time__lt = check_out) | Q(book_till_time__gt = check_in)) & Q(room_number = room.room_number) & Q(book_from_date = book_date))
            #taken = Customer.objects.filter((Q(book_from_time__lt = check_out) | Q(book_till_time__gt = check_in)), room_number = room.room_number, book_from_date = book_date)
            #taken = Customer.objects.filter(book_from_date = book_date, book_from_time__lt = check_out, book_till_time__gt = check_in) 
            print(room)
            print(taken)
            print(not taken)
            if not taken:
                #all_rooms = list()
                #global dict1
                if room.category not in dict1:
                    #first_room = list()
                    #first_room.append(room.room_number)
                    #global dict1
                    #dict1[room.category] = first_room
                    dict1[room.category] = room.room_number
                '''else:
                    all_rooms = dict1[room.category]
                    all_rooms.append(room.room_number)
                    #global dict1
                    dict1[room.category] = all_rooms'''
    print("vetgtegv")
    print(dict1)
    print("tyuuih")
    return dict1
'''        
                #for num in all_rooms:
                    properties = Room.objects.filter(room_number = num)
                    cat = list()
                    cat.append(properties.category)
                time_slot = Customer(user = username, book_from_date = book_date, book_from_time = check_in, book_till_time = check_out, room_number = booked_number, category = category, capacity = capacity)
                time_slot.save()
                return True
    return False'''
    
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
            global capacity
            capacity = request.POST['capacity']
            global converted_book_from_date
            converted_book_from_date = convert_to_date(book_from_date)
            global converted_book_from_time
            converted_book_from_time = convert_to_time(book_from_time)
            global converted_book_till_time
            converted_book_till_time = convert_to_time(book_till_time)
            to_let = dict()
            to_let = check_availability(category, converted_book_from_date, converted_book_from_time, converted_book_till_time, now, capacity)
            if to_let != {}:
                response = to_let.keys()
                #return HttpResponse(to_let.keys())
                '''response = 'Blogs:'
                for blog in to_let.keys():
                    response += '<br \> {0}'.format(blog)
                #return HttpResponse(response)'''
                context = {'categories': response}
                return render(request, 'suss.html', context)
                return HttpResponse("Booked")
            return HttpResponse("Not Booked")
        else:
            context = {'form': AvailabilityForm()}
            return render(request, 'book.html', context)
    context = {'form': AvailabilityForm()}
    return render(request, 'book.html', context)
    
def yac(request):
    if request.method == 'POST':
        time_slot = Customer(user = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['YAC'], category = 'YAC', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'yac.html')
