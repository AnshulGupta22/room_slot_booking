from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from hotel.forms import CustomerForm, SigninForm, BookingForm
from django.http import HttpResponse
from . models import Customer, Room, Booking
import datetime
from django.db.models import Q
from django.utils import timezone

# Create your views here.

#username = ''
username = None
#registered = 0
#now = datetime.datetime(2015, 10, 29, 23, 55, 59, 342380)
now = None
converted_book_from_date = None
converted_book_from_time = None
converted_book_till_time = None
capacity = None
'''
converted_book_from_date = datetime.date(1996, 12, 11)
converted_book_from_time = datetime.time(13, 24, 56)
converted_book_till_time = datetime.time(13, 24, 56)
'''
dict1 = None

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
        form = CustomerForm(request.POST)
        if form.is_valid() and request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.create_user(request.POST['desired_username'],  request.POST['email'], request.POST['password'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                global username
                username = request.POST['desired_username']
                #global registered
                #registered = 1
                login(request, user)
                return redirect('../book/')
            except:
       	        return HttpResponse("Username already exist")
        else:
            context = {'form': form}
            return render(request, 'signup.html', context)
    context = {'form': CustomerForm()}
    return render(request, 'signup.html', context)

def sign_in(request):
    #global registered
    #if registered == 0:
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
    #else:
    #    return redirect('../book/')

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    #return render(request,'logout.html')
    return redirect('../signin/')
    
#def check_availability(book_date, check_in, check_out, now, capacity):
def check_availability(book_date, check_in, check_out, capacity):
    global dict1
    dict1 = dict()
    room_list = Room.objects.filter(available_from__lte = check_in, available_till__gte =  check_out, capacity__gte = capacity)
    print("vetgtegv")
    print(room_list)
    print("tgevd")
    #global now
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            added_check_out = check_out.replace(hour=(check_out.hour+1) % 24)
            subtracted_check_in = check_in.replace(hour=(check_in.hour-1) % 24)
            #print(added_check_out)
            #This logic works for a particular room
            taken = Booking.objects.filter(Q(Q(book_from_time__lt = added_check_out) | Q(book_till_time__gt = subtracted_check_in)) & Q(room_number = room.room_number) & Q(book_from_date = book_date))
            #taken = Customer.objects.filter((Q(book_from_time__lt = check_out) | Q(book_till_time__gt = check_in)), room_number = room.room_number, book_from_date = book_date)
            #taken = Customer.objects.filter(book_from_date = book_date, book_from_time__lt = check_out, book_till_time__gt = check_in) 
            '''print(room)
            print(taken)
            print(not taken)'''
            print(taken)
            if not taken:
                #all_rooms = list()
                #global dict1
                print("bhvla")
                print(taken)
                print(room.category)
                print(dict1)
                if room.category not in dict1:
                    #first_room = list()
                    #first_room.append(room.room_number)
                    #global dict1
                    dict1[room.category] = room.room_number
            
                    '''print("jvcd")
                    print(dict1) 
                    print("xdvbh")'''     
                '''else:
                    all_rooms = dict1[room.category]
                    all_rooms.append(room.room_number)
                    #global dict1
                    dict1[room.category] = all_rooms'''
    '''print("vetgtegv")
    print(dict1)
    print("tyuuih")'''
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
        form = BookingForm(request.POST)
        if form.is_valid():
            global now
            #now = datetime.datetime.now()
            now = timezone.now()
            
            print("gteg")
            print(now)
            #print(rgv)
            print("vnhhhf")
            #nextD = now + datetime.timedelta(days=5)
            #print(nextD)
            #print(now+1)
            book_from_date = request.POST['book_from_date']
            book_from_time = request.POST['book_from_time']
            book_till_time = request.POST['book_till_time']
            global capacity
            capacity = request.POST['capacity']
            global converted_book_from_date
            converted_book_from_date = convert_to_date(book_from_date)
            global converted_book_from_time
            converted_book_from_time = convert_to_time(book_from_time)
            global converted_book_till_time
            converted_book_till_time = convert_to_time(book_till_time)
            to_let = dict()
            #to_let = check_availability(converted_book_from_date, converted_book_from_time, converted_book_till_time, now, capacity)
            to_let = check_availability(converted_book_from_date, converted_book_from_time, converted_book_till_time, capacity)
            if to_let != {}:
                response = to_let.keys()
                #return HttpResponse(to_let.keys())
                '''response = 'Blogs:'
                for blog in to_let.keys():
                    response += '<br \> {0}'.format(blog)
                #return HttpResponse(response)'''
                context = {'categories': response}
                return render(request, 'categories.html', context)
            return HttpResponse("Not Available")
        else:
            context = {'form': BookingForm()}
            return render(request, 'book.html', context)
    context = {'form': BookingForm()}
    return render(request, 'book.html', context)
   
@login_required(login_url="/hotel/signin/") 
def yac(request):
    time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['YAC'], category = 'YAC', capacity = capacity)
    time_slot.save()
    return HttpResponse("Booked")
    '''
    if request.method == 'POST':
        time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['YAC'], category = 'YAC', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'yac.html')'''
    
@login_required(login_url="/hotel/signin/")
def nac(request):
    time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['NAC'], category = 'NAC', capacity = capacity)
    time_slot.save()
    return HttpResponse("Booked")
    '''
    if request.method == 'POST':
        time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['NAC'], category = 'NAC', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'nac.html')'''
    
@login_required(login_url="/hotel/signin/")
def deluxe(request):
    time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['DEL'], category = 'DEL', capacity = capacity)
    time_slot.save()
    return HttpResponse("Booked")
    '''
    if request.method == 'POST':
        time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['DEL'], category = 'DEL', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'deluxe.html')'''
    
@login_required(login_url="/hotel/signin/")
def king(request):
    time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['KIN'], category = 'KIN', capacity = capacity)
    time_slot.save()
    return HttpResponse("Booked")
    '''
    if request.method == 'POST':
        time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['KIN'], category = 'KIN', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'king.html')'''
    
@login_required(login_url="/hotel/signin/")
def queen(request):
    time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['QUE'], category = 'QUE', capacity = capacity)
    time_slot.save()
    return HttpResponse("Booked")
    
@login_required(login_url="/hotel/signin/")
def future(request, booking_id=None):
    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
        except:   
            return HttpResponse("This booking no longer exists.")
    else:
        global now
        now = timezone.now()
#fur_dat = now.replace(day=(now.day+1) % )
        booking_objects = Booking.objects.filter(customer_name = username, book_from_date__gte = now.date())
        context = {'future_bookings': booking_objects}
        return render(request, 'future_bookings.html', context)
    
@login_required(login_url="/hotel/signin/")
def all_bookings(request):
    all_booking_objects = Booking.objects.filter(customer_name = username)
    context = {'all_bookings': all_booking_objects}
    return render(request, 'all_bookings.html', context)
    '''
    if request.method == 'POST':
        time_slot = Booking(customer_name = username, book_from_date = converted_book_from_date, book_from_time = converted_book_from_time, book_till_time = converted_book_till_time, room_number = dict1['QUE'], category = 'QUE', capacity = capacity)
        time_slot.save()
        return HttpResponse("Booked")
    return render(request, 'queen.html')'''
#print(future_bookings)
    #future_bookings = Booking.objects.get(customer_name = username, book_from_date__gte = now.date())
    '''for fields in future_bookings:
        print(fields.customer_name)
        print(fields.book_from_date)
        print(fields.book_from_time)
        print(fields.book_till_time)
        print(fields.room_number)
        print(fields.category)
        print(fields.capacity)
        #customer_bookings = "Date: " + fields.book_from_date + "\nCheck-in time: " + fields.book_from_time + "\nCheck-out time: " + fields.book_till_time + "\nPeople: " + fields.capacity + "\Category: " + fields.category +"\n"
        #print(customer_bookings)'''
    #print(booking_objects)
    #return HttpResponse(booking_objects)
