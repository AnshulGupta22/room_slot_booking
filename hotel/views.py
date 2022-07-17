from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth.models import User
from hotel.forms import CustomerForm, SignInForm, BookingForm
from . models import Customer, Room, Booking

# Create your views here.

username = None
now = None
book_date = None
check_in = None
check_out = None
capacity = None
available_categories = None

"""Function to convert string to date."""
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    datetime_str = datetime.datetime.strptime(date_time, format).date()
    return datetime_str

"""Function to convert string to time."""
def convert_to_time(date_time):
    format = '%H:%M'
    datetime_str = datetime.datetime.strptime(date_time, format).time()
    return datetime_str

"""Function to go to home page."""
def home(request):
    return render(request,'home.html')
    
"""Function for sign up."""
def sign_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if (form.is_valid() and 
            request.POST['password'] == request.POST['confirm_password']):
            try:
                user = User.objects.create_user(
                    request.POST['desired_username'], 
                    request.POST['email'], request.POST['password']
                    )
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
            except:
       	        return HttpResponse("Username already exist")
       	    global username
            username = request.POST['desired_username']
            login(request, user)
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'signup.html', context)
    context = {'form': CustomerForm()}
    return render(request, 'signup.html', context)

"""Function for sign in."""
def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
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
    context = {'form': SignInForm()}
    return render(request, 'signin.html', context)

"""Function for log out."""
def logout_view(request):
    logout(request)
    return redirect('../signin/')

"""Function that returns the list of available categories."""
def check_availability():
    global available_categories
    available_categories = list()
    room_list = Room.objects.filter(
        available_from__lte=check_in, 
        available_till__gte=check_out, 
        capacity__gte=capacity
        )
    for room in room_list:
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = check_out.replace(
                hour = (check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour = (check_in.hour- 1 ) % 24
            )
            # Checking if the room is already booked.
            taken = Booking.objects.filter(Q(Q(book_from_time__lt=added_check_out)
                                           | Q(book_till_time__gt=subtracted_check_in)) 
                                           & Q(room_number=room.room_number) 
                                           & Q(book_from_date=book_date))
            if not taken:
                if room.category not in available_categories:
                    # Appending available category.
                    available_categories.append(room.category)
    return available_categories

"""Function to return the available categories."""
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            global now
            now = timezone.now()
            book_from_date = request.POST['book_from_date']
            book_from_time = request.POST['book_from_time']
            book_till_time = request.POST['book_till_time']
            global capacity
            capacity = request.POST['capacity']
            global book_date
            book_date = convert_to_date(book_from_date)
            global check_in
            check_in = convert_to_time(book_from_time)
            global check_out
            check_out = convert_to_time(book_till_time)
            to_let = list()
            to_let = check_availability()
            if to_let:
                response = to_let
                context = {'categories': response}
                return render(request, 'categories.html', context)
            return HttpResponse("Not Available")
        else:
            context = {'form': BookingForm()}
            return render(request, 'book.html', context)
    context = {'form': BookingForm()}
    return render(request, 'book.html', context)
   
"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def yac(request):
    # List of rooms for the given category.
    room_list = Room.objects.filter(
        available_from__lte = check_in, 
        available_till__gte =  check_out, 
        capacity__gte = capacity, category = 'YAC'
        )
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = check_out.replace(    
                hour=(check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour=(check_in.hour - 1) % 24
                )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt = added_check_out) 
                | Q(book_till_time__gt = subtracted_check_in)) 
                & Q(room_number = room.room_number) 
                & Q(book_from_date = book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=username, 
                    book_from_date=book_date, 
                    book_from_time=check_in, 
                    book_till_time=check_out, 
                    room_number=room.room_number, 
                    category='YAC', capacity=capacity
                    )
                time_slot.save()
                return render(request, 'booked.html')
    return HttpResponse("Not available")
    
"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def nac(request):
    # List of rooms for the given category.
    room_list = Room.objects.filter(
        available_from__lte=check_in, 
        available_till__gte=check_out, 
        capacity__gte=capacity, category='NAC'
        )
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = check_out.replace(
                hour=(check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour=(check_in.hour- 1 ) % 24
                )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt=added_check_out) 
                | Q(book_till_time__gt=subtracted_check_in)) 
                & Q(room_number=room.room_number) 
                & Q(book_from_date=book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=username, 
                    book_from_date=book_date, 
                    book_from_time=check_in, 
                    book_till_time=check_out, 
                    room_number=room.room_number, 
                    category='NAC', capacity=capacity
                    )
                time_slot.save()
                return render(request, 'booked.html')
    return HttpResponse("Not available")
    
"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def deluxe(request):
    # List of rooms for the given category
    room_list = Room.objects.filter(
        available_from__lte=check_in, 
        available_till__gte=check_out, 
        capacity__gte=capacity, category = 'DEL'
        )
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out=check_out.replace(
                hour=(check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour=(check_in.hour - 1) % 24
                )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt=added_check_out) 
                | Q(book_till_time__gt=subtracted_check_in)) 
                & Q(room_number=room.room_number) 
                & Q(book_from_date=book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=username, 
                    book_from_date=book_date, 
                    book_from_time=check_in, 
                    book_till_time=check_out, 
                    room_number=room.room_number, 
                    category='DEL', capacity=capacity
                    )
                time_slot.save()
                return render(request, 'booked.html')
    return HttpResponse("Not available")
    
"""Function to book room of this category if available."""
@login_required(login_url = "/hotel/signin/")
def king(request):
    # List of rooms for the given category.
    room_list = Room.objects.filter(
        available_from__lte=check_in, 
        available_till__gte= check_out, 
        capacity__gte=capacity, category='KIN'
        )
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = check_out.replace(
                hour=(check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour=(check_in.hour - 1) % 24
                )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt=added_check_out) 
                | Q(book_till_time__gt=subtracted_check_in)) 
                & Q(room_number=room.room_number) 
                & Q(book_from_date=book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=username, 
                    book_from_date=book_date, 
                    book_from_time=check_in, 
                    book_till_time=check_out, 
                    room_number=room.room_number, 
                    category='KIN', capacity=capacity
                    )
                time_slot.save()
                return render(request,'booked.html')
    return HttpResponse("Not available")
    
"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def queen(request):
    # List of rooms for the given category
    room_list = Room.objects.filter(
        available_from__lte=check_in, 
        available_till__gte=check_out, 
        capacity__gte=capacity, category='QUE'
        )
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if(book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = check_out.replace(
                hour = (check_out.hour + 1) % 24
                )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = check_in.replace(
                hour = (check_in.hour - 1 ) % 24
                )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt=added_check_out) 
                | Q(book_till_time__gt=subtracted_check_in)) 
                & Q(room_number=room.room_number) 
                & Q(book_from_date=book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=username, 
                    book_from_date=book_date, 
                    book_from_time=check_in, 
                    book_till_time=check_out, 
                    room_number=room.room_number, 
                    category='QUE', capacity=capacity
                    )
                time_slot.save()
                return render(request, 'booked.html')
    return HttpResponse("Not available")

"""Function to return all the bookings."""
@login_required(login_url="/hotel/signin/")
def all_bookings(request, booking_id=None):
    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)    
        except:   
            return HttpResponse("This booking no longer exists.")
        booking.delete()
    global now
    now = timezone.now()
    # Future bookings.
    future_bookings = Booking.objects.filter(
        customer_name=username, 
        book_from_date__gt=now.date()
        )
    # Current and past bookings.
    current_and_past_bookings = Booking.objects.filter(
        customer_name=username, book_from_date__lte=now.date()
        )
    context = {
        'future_bookings': future_bookings, 
        'current_and_past_bookings': current_and_past_bookings
        }
    return render(request, 'all_bookings.html', context)

