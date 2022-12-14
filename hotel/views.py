from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from hotel.forms import CustomerForm, SignInForm, BookingForm, RoomForm, ManageBookingForm, AddRoomForm, ManageViewTimeSlotForm, ViewTimeSlotForm, AddTimeSlotForm, EditRoomForm, EditForm
from .models import Room, Booking, TimeSlot

from .serializers import (
    RoomSerializer, BookingSerializerBook, BookingSerializerAdmin,
    BookingSerializerGet, BookingSerializerAdminWithoutid,
    CustomerAPISerializer, CustomerSerializer
    )

# Create your views here.

now = timezone.now()
'''
#request.session['api_username'] = ''
request.session['api_book_date'] = None

request.session['api_check_in'] = None

request.session['api_check_out'] = None

request.session['api_person'] = 1

request.session['api_username']
api_no_of_rooms_required = 1
request.session['api_username']
api_ac_rooms = 0
request.session['api_username']
api_nac_rooms = 0
request.session['api_username']
api_deluxe_rooms = 0
request.session['api_username']
api_king_rooms = 0
request.session['api_username']
api_queen_rooms = 0
'''


"""Function to convert string to date."""
def convert_to_date(date_time):
    format = '%Y-%m-%d'
    try:
        datetime_str = datetime.datetime.strptime(date_time, format).date()
    except Exception:
        datetime_str = None
    return datetime_str

"""Function to convert string to time."""
def convert_to_time_sec(date_time):
    format = '%H:%M:%S'
    try:
        datetime_str = datetime.datetime.strptime(date_time, format).time()
    except Exception:
        datetime_str = None
    return datetime_str

"""Function to convert string to time."""
def convert_to_time(date_time):
    format = '%H:%M'
    try:
        datetime_str = datetime.datetime.strptime(date_time, format).time()
    except Exception:
        datetime_str = None
    return datetime_str

"""Function to go to home page."""
def home(request):
    return render(request, 'home.html')

"""Function for sign up."""
def sign_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'], request.POST['password1']
                )
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
            except Exception:
                return HttpResponse("Something went wrong. Please try again.")
            login(request, user)
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'sign_up.html', context)
    context = {'form': CustomerForm()}
    return render(request, 'sign_up.html', context)

"""Function for viewing profile."""
@login_required(login_url="/hotel/signin/")
def view_profile(request):
    profile = User.objects.filter(
        username=request.user.username
        ).values()
    context = {'profile': profile}
    return render(request, 'view_profile.html', context)

"""Function for editing profile."""
@login_required(login_url="/hotel/signin/")
def edit_profile(request):
    profile = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'edit_profile.html', context)
    context = {'form': EditForm(instance=profile), 'username': request.user.username}
    return render(request, 'edit_profile.html', context)

"""Function for sign in."""
def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            user = authenticate(
                request, username=request.POST['username'], password=password
                )
            login(request, user)
            if user.is_superuser:
                return redirect('../manage/')
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'sign_in.html', context)
    context = {'form': SignInForm()}
    return render(request, 'sign_in.html', context)

"""Function to display room manager options."""
@login_required(login_url="/hotel/signin/")
def manage(request):
    if request.user.email.endswith("@anshul.com"):
        context = {
            'username': request.user.username
            }
        return render(request, 'manager.html', context)
    else:
        return redirect('../book/')

"""Function that returns the list of rooms based on the search criteria."""
def manager_room_search(
        str_room_numbers, categories, capacities, advance, username):
    #print(str_room_numbers)
    if str_room_numbers != '':
        spaces_room_numbers = list(str_room_numbers.split(","))
        room_numbers = list()
        for i in spaces_room_numbers:
            room_numbers.append(i.strip())
        #print(room_numbers)
    else:
        room_numbers = ''
    #available_from = convert_to_time(str_available_from)
    #available_till = convert_to_time(str_available_till)
    #room_list = list()
    #for category in categories:
    '''room_list = Room.objects.filter(
        room_number=room_number,
        category=categories,
        available_from__lte=available_from,
        available_till__gte=available_till,
        capacity__gte=capacities,
        advance__gte=advance
    )'''
    #print(categories)
    '''if categories == []:
        categories = ['Regular', 'Executive', 'Deluxe', 'King', 'Queen']
    if capacities == []:
        capacities = [1, 2, 3, 4]
    if advance is None:
        advance = 0
    if available_from is None and available_till is None:
        room_list = Room.objects.filter(
        category__in=categories,
        capacity__in=capacities,
        advance__gte=advance
    )
    elif available_from is None:
        room_list = Room.objects.filter(
        category__in=categories,
        available_till__gte=available_till,
        capacity__in=capacities,
        advance__gte=advance
    )
    elif available_till is None:
        room_list = Room.objects.filter(
        category__in=categories,
        available_from__lte=available_from,
        capacity__in=capacities,
        advance__gte=advance
    )
    else:'''

    '''keys = ['room_number__in', 'category__in', 'available_from__lte', 'available_till__gte', 'capacity__in', 'advance__gte', 'room_manager']
    values = [room_numbers, categories, available_from, available_till, capacities, advance, username]'''
    keys = ['room_number__in', 'category__in', 'capacity__in', 'advance__gte', 'room_manager']
    values = [room_numbers, categories, capacities, advance, username]
    parameters = {}
    #temp = {'category__in': categories, 'available_from__lte': available_from, 'available_till__gte': available_till, 'capacity__in': capacities, 'advance__gte': advance}
    for key, value in zip(keys, values):
        if value is not None and value !=[] and value != '':
            parameters[key] = value
    #for key, value in temp:
    #    if value is not None and value !=[]:
    #        parameters[key] = value
    #print(room_numbers)
    room_list = Room.objects.filter(**parameters)
    #print("hwqaf")
    '''room_list = Room.objects.filter(
        category__in=categories,
        available_from__lte=available_from,
        available_till__gte=available_till,
        capacity__in=capacities,
        advance__gte=advance
    )'''
    #print(room_list)
    return room_list
        #select * from ROOM where db_room_number = room_number and db_category IN category and db_capacity IN capacity and db_available_from <= available_from and db_available_till >= available_till and db_advance >= advance
    """print(room_list)
    for capacity in capacities:
        room_list += Room.objects.filter(
            room_number=room_number,
            category=category,
            available_from__lte=available_from,
            available_till__gte=available_till,
            #capacity__gte=capacity,
            advance=advance
        )
    
    for room in room_list:
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + datetime.timedelta(days=room.advance)
        if (book_date <= max_book.date()):
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
            # Checking if the room is already booked.
            taken = Booking.objects.filter(Q(Q(check_in_time__lt=added_check_out)
                                             | Q(check_out_time__gt=subtracted_check_in))
                                           & Q(room_number__contains=room.room_number)
                                           & Q(check_in_date=book_date))
            if not taken:
                if (room.category == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                elif (room.category == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                elif (room.category == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                elif (room.category == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                elif (room.category == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
    if (normal_regular_rooms >= normal_no_of_rooms_required):
        available_categories.append('Regular')
    if (normal_executive_rooms >= normal_no_of_rooms_required):
        available_categories.append('Executive')
    if (normal_deluxe_rooms >= normal_no_of_rooms_required):
        available_categories.append('Deluxe')
    if (normal_king_rooms >= normal_no_of_rooms_required):
        available_categories.append('King')
    if (normal_queen_rooms >= normal_no_of_rooms_required):
        available_categories.append('Queen')
    return available_categories"""

"""Function to display rooms based on the selected criteria."""
@login_required(login_url="/hotel/signin/")
def manage_rooms(request):
    if request.user.email.endswith("@anshul.com"):
        rooms = Room.objects.filter(room_manager=request.user.username)
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                try:
                    request.session['room_numbers'] = request.POST['room_numbers']
                    print(request.session['room_numbers'])
                    #request.session['room_number'] = int(request.POST['room_number'])
                except Exception:
                    request.session['room_numbers'] = ''
                request.session['category'] = form.cleaned_data.get("category")
                str_capacity = form.cleaned_data.get("capacity")
                # using list comprehension to
                # perform conversion
                try:
                    request.session['capacity'] = [int(i) for i in str_capacity]
                except Exception:
                    request.session['capacity'] = None
                #request.session['available_from'] = request.POST['available_from']
                #request.session['available_till'] = request.POST['available_till']
                try:
                    request.session['advance'] = int(request.POST['advance'])
                except Exception:
                    request.session['advance'] = None
                #print(request.POST['room_numbers'])
                response = manager_room_search(request.session['room_numbers'],
                                        request.session['category'],
                                        request.session['capacity'],
                                        #request.session['available_from'],
                                        #request.session['available_till'],
                                        request.session['advance'],
                                        request.user.username)
                #if response:
                context = {
                    'form': form,
                    'rooms': response,
                    'username': request.user.username
                    }
                return render(request, 'manage_rooms.html', context)
                #return HttpResponse("Not Available")
            else:
                context = {
                    'form': form,
                    'rooms': None,
                    'username': request.user.username
                    }
                return render(request, 'manage_rooms.html', context)
        context = {
                'form': RoomForm(),
                'rooms': rooms,
                'username': request.user.username
                }
        return render(request, 'manage_rooms.html', context)
    else:
        return redirect('../book/')

"""Function to add/ edit room."""
'''
@login_required(login_url="/hotel/signin/")
def add_rooms(request, room_number=None):
    if request.user.email.endswith("@anshul.com"):
        if room_number:
            room = Room.objects.get(room_number=room_number)
        else:
            room = Room()

        if request.method == 'POST':

            if room_number:
                form = EditRoomForm(request.POST, instance=room)
            else:
                form = AddRoomForm(request.POST, instance=room)
            
            if form.is_valid():
                room = Room(room_number=request.POST['room_number'],
                        category=request.POST['category'],
                        capacity=request.POST['capacity'],
                        #available_from=request.POST['available_from'],
                        #available_till=request.POST['available_till'],
                        advance=request.POST['advance'],
                        room_manager=request.user.username)
                room.save()
                # Implemented Post/Redirect/Get.
                if room_number:
                    return redirect('../../manage_rooms/')
                return redirect('../manage_rooms/')
                #return render(request, 'manage_rooms.html', context)
            else:
                context = {
                    'form': form,
                    'username': request.user.username
                    }
                return render(request, 'add_rooms.html', context)
        context = {
                'form': AddRoomForm(instance=room),
                'username': request.user.username
                }
        return render(request, 'add_rooms.html', context)
    else:
        return redirect('../book/')
'''














"""Function to add/ edit room."""
@login_required(login_url="/hotel/signin/")
def add_rooms(request):
    if request.user.email.endswith("@anshul.com"):
        room = Room()
        if request.method == 'POST':
            form = AddRoomForm(request.POST, instance=room)
            if form.is_valid():
                room = Room(room_number=request.POST['room_number'],
                        category=request.POST['category'],
                        capacity=request.POST['capacity'],
                        #available_from=request.POST['available_from'],
                        #available_till=request.POST['available_till'],
                        advance=request.POST['advance'],
                        room_manager=request.user.username)
                room.save()

                '''form = RoomForm()
                context = {
                    'form': form,
                    'rooms': Room.objects.filter(room_manager=request.user.username),
                    'username': request.user.username
                    }'''
                # Implemented Post/Redirect/Get.
                return redirect('../manage_rooms/')
                #return render(request, 'manage_rooms.html', context)
            else:
                context = {
                    'form': form,
                    'username': request.user.username
                    }
                return render(request, 'add_rooms.html', context)
        '''context = {
                'form': AddRoomForm(),
                'username': request.user.username
                }'''
        context = {
                'form': AddRoomForm(instance=room),
                'username': request.user.username
                }
        return render(request, 'add_rooms.html', context)
    else:
        return redirect('../book/')









"""Function to add/ edit room."""
@login_required(login_url="/hotel/signin/")
def edit_rooms(request, room_number=None):
    if request.user.email.endswith("@anshul.com"):
        if room_number:
            try:
                room = Room.objects.get(room_number=room_number, room_manager=request.user.username)
            except Exception:
                return HttpResponse("Bad request.")
        else:
            return HttpResponse("Bad request.")

        if request.method == 'POST':

            form = EditRoomForm(request.POST, instance=room)
            
            if form.is_valid():
                room = Room(room_number=request.POST['room_number'],
                        category=request.POST['category'],
                        capacity=request.POST['capacity'],
                        advance=request.POST['advance'],
                        room_manager=request.user.username)
                room.save()

                # Implemented Post/Redirect/Get.
                if room_number:
                    return redirect('../../manage_rooms/')
            else:
                context = {
                    'form': form,
                    'username': request.user.username
                    }
                return render(request, 'edit_rooms.html', context)
        context = {
                'form': EditRoomForm(instance=room),
                'username': request.user.username
                }
        return render(request, 'edit_rooms.html', context)
    else:
        return redirect('../book/')

"""Function to add/ edit time_slot."""
@login_required(login_url="/hotel/signin/")
def add_time_slots(request, room_number):
    if request.user.email.endswith("@anshul.com"):
        if request.method == 'POST':
            form = AddTimeSlotForm(request.POST)
            if form.is_valid():
                try:
                    room_obj = Room.objects.get(room_number=room_number, room_manager=request.user.username)
                except Exception:
                    return HttpResponse("Bad request.")

                available_till = convert_to_time(request.POST['available_till'])
                available_from = convert_to_time(request.POST['available_from'])

                # To ensure no rooms are booked within a gap of 1 hour
                # after checkout.
                added_available_till = available_till.replace(
                    hour=(available_till.hour + 1) % 24
                )
                
                # To ensure no rooms are booked within a gap of 1 hour
                # before checkin.
                subtracted_available_from = available_from.replace(
                    hour=(available_from.hour - 1) % 24
                )

                taken = TimeSlot.objects.filter(Q(room=room_obj)
                                             & (Q(Q(available_till__gt=subtracted_available_from)
                                             & Q(available_from__lte=subtracted_available_from))
                                             | Q(Q(available_from__lt=added_available_till)
                                             & Q(available_till__gte=added_available_till))
                                             | Q(Q(available_from__gte=subtracted_available_from)
                                             & Q(available_till__lte=added_available_till))))
                if not taken:
                    time_slot = TimeSlot(room=room_obj,
                            available_from=available_from,
                            available_till=available_till)
                    time_slot.save()
                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../view_time_slots/{room_obj.room_number}/')
                else:
                    return HttpResponse("Time slot not available.")
            else:
                context = {
                    'form': form,
                    'room_number': room_number,
                    'username': request.user.username
                    }
                return render(request, 'add_time_slots.html', context)
        context = {
                'form': AddTimeSlotForm(),
                'room_number': room_number,
                'username': request.user.username
                }
        return render(request, 'add_time_slots.html', context)
    else:
        return redirect('../book/')

"""Function to add/ edit time_slot."""
@login_required(login_url="/hotel/signin/")
def edit_time_slots(request, pk):
    if request.user.email.endswith("@anshul.com"):
        if pk:
            try:
                #time_slot_obj = TimeSlot.objects.get(pk=pk)
                time_slot_obj = TimeSlot.objects.get(Q(pk=pk) & Q(occupancy='Vacant'))
            except Exception:
                return HttpResponse("Bad request.")
        else:
            return HttpResponse("Bad request.")
        if time_slot_obj.room.room_manager != request.user.username:
            return HttpResponse("Bad request.")
        #if time_slot_obj.occupancy == 'Booked':
            #return HttpResponse("Bad request.")
        if request.method == 'POST':
            form = AddTimeSlotForm(request.POST, instance=time_slot_obj)
            if form.is_valid():
                try:
                    Room.objects.get(room_number=time_slot_obj.room.room_number, room_manager=request.user.username)
                except Exception:
                    return HttpResponse("Bad request.")
                #print(type(request.POST['available_from']))
                #print(request.POST['available_till'])
                available_till = convert_to_time_sec(request.POST['available_till'])
                available_from = convert_to_time_sec(request.POST['available_from'])
                #print(available_till)
                #print(available_from)
                # To ensure no rooms are booked within a gap of 1 hour
                # after checkout.
                added_available_till = available_till.replace(
                    hour=(available_till.hour + 1) % 24
                )

                # To ensure no rooms are booked within a gap of 1 hour
                # before checkin.
                subtracted_available_from = available_from.replace(
                    hour=(available_from.hour - 1) % 24
                )

                taken = TimeSlot.objects.filter(Q(room=time_slot_obj.room)
                                             & (Q(Q(available_till__gt=subtracted_available_from)
                                             & Q(available_from__lte=subtracted_available_from))
                                             | Q(Q(available_from__lt=added_available_till)
                                             & Q(available_till__gte=added_available_till))
                                             | Q(Q(available_from__gte=subtracted_available_from)
                                             & Q(available_till__lte=added_available_till))))
                if not taken:
                    time_slot_obj.available_from = available_from
                    time_slot_obj.available_till = available_till
                    time_slot_obj.save()
                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../view_time_slots/{time_slot_obj.room.room_number}/')
                else:
                    if taken.count() == 1:
                        for record in taken:
                            if record.pk == time_slot_obj.pk and time_slot_obj.available_from <= available_from and time_slot_obj.available_till >= available_till:
                                time_slot_obj.available_from = available_from
                                time_slot_obj.available_till = available_till
                                time_slot_obj.save()
                                # Implemented Post/Redirect/Get.
                                return redirect(f'../../view_time_slots/{time_slot_obj.room.room_number}/')
                            else:
                                return HttpResponse("Time slot not available.")
                    else:
                        return HttpResponse("Time slot not available.")
                    #if record.pk == time_slot_obj.pk or not taken:
                    #print(time_slot_obj.pk) & Q(time_slot_obj.pk=time_slot_obj.pk)
                    '''if not taken:
                    time_slot_obj.available_from = available_from
                    time_slot_obj.available_till = available_till
                    time_slot_obj.save()
                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../view_time_slots/{time_slot_obj.room.room_number}/')
                    elif record.pk == time_slot_obj.pk and time_slot_obj.available_from <= available_from and time_slot_obj.available_till >= available_till:
                    time_slot_obj.available_from = available_from
                    time_slot_obj.available_till = available_till
                    time_slot_obj.save()
                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../view_time_slots/{time_slot_obj.room.room_number}/')'''                
            else:
                context = {
                    'form': form,
                    'username': request.user.username,
                    'room_number': time_slot_obj.room.room_number
                    }
                return render(request, 'add_time_slots.html', context)
        context = {
                'form': AddTimeSlotForm(instance=time_slot_obj),
                'username': request.user.username,
                'room_number': time_slot_obj.room.room_number
                }
        return render(request, 'edit_time_slots.html', context)
    else:
        return redirect('../book/')

"""Function to delete room."""
@login_required(login_url="/hotel/signin/")
def delete_time_slot(request, pk):
    if request.user.email.endswith("@anshul.com"):
        if pk:
            try:
                time_slot_obj = TimeSlot.objects.get(Q(pk=pk) & Q(occupancy='Vacant'))
            except Exception:
                return HttpResponse("Not found.")
            if time_slot_obj.room.room_manager != request.user.username:
                return HttpResponse("Bad request.")
            time_slot_obj.delete()
            # Implemented Post/Redirect/Get.
            return redirect(f'../../view_time_slots/{time_slot_obj.room.room_number}/')
        else:
            return HttpResponse("Not found.")
    else:
        return redirect('../book/')

"""Function that returns the list of rooms based on the search criteria."""
def manager_time_slot_search(
        room_number, str_available_from, str_available_till, occupancy):
    room_obj = Room.objects.get(room_number=room_number)
    #print(str_available_from)
    '''if str_room_numbers != '':
        spaces_room_numbers = list(str_room_numbers.split(","))
        room_numbers = list()
        for i in spaces_room_numbers:
            room_numbers.append(i.strip())
        #print(room_numbers)
    else:
        room_numbers = '''''
    available_from = convert_to_time(str_available_from)
    available_till = convert_to_time(str_available_till)
    #room_list = list()
    #for category in categories:
    '''room_list = Room.objects.filter(
        room_number=room_number,
        category=categories,
        available_from__lte=available_from,
        available_till__gte=available_till,
        capacity__gte=capacities,
        advance__gte=advance
    )'''
    #print(categories)
    '''if categories == []:
        categories = ['Regular', 'Executive', 'Deluxe', 'King', 'Queen']
    if capacities == []:
        capacities = [1, 2, 3, 4]
    if advance is None:
        advance = 0
    if available_from is None and available_till is None:
        room_list = Room.objects.filter(
        category__in=categories,
        capacity__in=capacities,
        advance__gte=advance
    )
    elif available_from is None:
        room_list = Room.objects.filter(
        category__in=categories,
        available_till__gte=available_till,
        capacity__in=capacities,
        advance__gte=advance
    )
    elif available_till is None:
        room_list = Room.objects.filter(
        category__in=categories,
        available_from__lte=available_from,
        capacity__in=capacities,
        advance__gte=advance
    )
    else:'''
    #print(available_from)
    '''keys = ['room_number__in', 'category__in', 'available_from__lte', 'available_till__gte', 'capacity__in', 'advance__gte', 'room_manager']
    values = [room_numbers, categories, available_from, available_till, capacities, advance, username]'''
    if available_till is None:
        keys = ['room', 'available_from__lte', 'available_till__gt', 'occupancy']
        values = [room_obj, available_from, available_from, occupancy]

    elif available_from is None:
        keys = ['room', 'available_from__lt', 'available_till__gte', 'occupancy']
        values = [room_obj, available_till, available_till, occupancy]
    else:
        keys = ['room', 'available_from__lte', 'available_till__gte', 'occupancy']
        values = [room_obj, available_from, available_till, occupancy]
    parameters = {}
    #temp = {'category__in': categories, 'available_from__lte': available_from, 'available_till__gte': available_till, 'capacity__in': capacities, 'advance__gte': advance}
    for key, value in zip(keys, values):
        if value is not None and value !=[] and value != '':
            parameters[key] = value
    #for key, value in temp:
    #    if value is not None and value !=[]:
    #        parameters[key] = value
    #print(parameters)
    time_slots_list = TimeSlot.objects.filter(**parameters)
    #print("hwqaf")
    '''room_list = Room.objects.filter(
        category__in=categories,
        available_from__lte=available_from,
        available_till__gte=available_till,
        capacity__in=capacities,
        advance__gte=advance
    )'''
    #print(time_slots_list)
    return time_slots_list
        #select * from ROOM where db_room_number = room_number and db_category IN category and db_capacity IN capacity and db_available_from <= available_from and db_available_till >= available_till and db_advance >= advance
    """print(room_list)
    for capacity in capacities:
        room_list += Room.objects.filter(
            room_number=room_number,
            category=category,
            available_from__lte=available_from,
            available_till__gte=available_till,
            #capacity__gte=capacity,
            advance=advance
        )
    
    for room in room_list:
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + datetime.timedelta(days=room.advance)
        if (book_date <= max_book.date()):
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
            # Checking if the room is already booked.
            taken = Booking.objects.filter(Q(Q(check_in_time__lt=added_check_out)
                                             | Q(check_out_time__gt=subtracted_check_in))
                                           & Q(room_number__contains=room.room_number)
                                           & Q(check_in_date=book_date))
            if not taken:
                if (room.category == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                elif (room.category == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                elif (room.category == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                elif (room.category == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                elif (room.category == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
    if (normal_regular_rooms >= normal_no_of_rooms_required):
        available_categories.append('Regular')
    if (normal_executive_rooms >= normal_no_of_rooms_required):
        available_categories.append('Executive')
    if (normal_deluxe_rooms >= normal_no_of_rooms_required):
        available_categories.append('Deluxe')
    if (normal_king_rooms >= normal_no_of_rooms_required):
        available_categories.append('King')
    if (normal_queen_rooms >= normal_no_of_rooms_required):
        available_categories.append('Queen')
    return available_categories"""

"""Function to add/ edit time_slot."""
@login_required(login_url="/hotel/signin/")
def view_time_slots(request, room_number):
    if request.user.email.endswith("@anshul.com"):
        '''if room_number:
            time_slot = TimeSlot.objects.get(room_number=room_number)
        else:
            time_slot = TimeSlot()'''
        try:
            room = Room.objects.get(room_number=room_number, room_manager=request.user.username)
        except Exception:
            return HttpResponse("Bad request.")
        if request.method == 'POST':
            form = ViewTimeSlotForm(request.POST)
            if form.is_valid():
                #print("bgyjm")
                #print(form.cleaned_data.get("booked"))
                #request.session['booked'] = form.cleaned_data.get("booked")
                '''booked = True
                try:
                    request.POST['booked']
                except Exception:
                    booked = False'''
                '''try:
                    request.session['room_numbers'] = request.POST['room_numbers']
                    #print(request.session['room_numbers'])
                    #request.session['room_number'] = int(request.POST['room_number'])
                except Exception:
                    request.session['room_numbers'] = ''
                request.session['category'] = form.cleaned_data.get("category")
                str_capacity = form.cleaned_data.get("capacity")
                # using list comprehension to
                # perform conversion
                try:
                    request.session['capacity'] = [int(i) for i in str_capacity]
                except Exception:
                    request.session['capacity'] = None'''
                #print(request.POST['available_from'])
                request.session['available_from'] = request.POST['available_from']
                request.session['available_till'] = request.POST['available_till']
                request.session['occupancy'] = form.cleaned_data.get("occupancy")
                #print(request.session['booked'])
                '''try:
                    request.session['advance'] = int(request.POST['advance'])
                except Exception:
                    request.session['advance'] = None'''
                time_slots = manager_time_slot_search(room_number,
                                        request.session['available_from'],
                                        request.session['available_till'], request.session['occupancy']
                                        )
                #if response:
                #print(time_slots)
                context = {
                    'form': form,
                    'room': room,
                    'time_slots': time_slots,
                    'username': request.user.username
                    }
                return render(request, 'view_time_slots.html', context)
                #return HttpResponse("Not Available")
            else:
                context = {
                    'form': form,
                    'room': room,
                    'time_slots': None,
                    'username': request.user.username
                    }
                return render(request, 'view_time_slots.html', context)
        context = {
                'form': ViewTimeSlotForm(),
                'room': room,
                #'room_number': room_number,
                #'time_slots': TimeSlot.objects.filter(room=room_number, room_manager=request.user.username),
                'time_slots': TimeSlot.objects.filter(room_id=room_number),
                'username': request.user.username
                }
        return render(request, 'view_time_slots.html', context)
    else:
        return redirect('../book/')

"""Function to add/ edit time_slot."""
@login_required(login_url="/hotel/signin/")
def manage_time_slots(request):
    if request.user.email.endswith("@anshul.com"):
        '''if room_number:
            time_slot = TimeSlot.objects.get(room_number=room_number)
        else:
            time_slot = TimeSlot()'''
        asd = TimeSlot.objects.all()
        print(asd)
        for course in asd:
            print(course['category'])
            #print(getattr(course, 'category'))
        if request.method == 'POST':
            form = ManageViewTimeSlotForm(request.POST)
            if form.is_valid():
                try:
                    request.session['room_numbers'] = request.POST['room_numbers']
                    #print(request.session['room_numbers'])
                    #request.session['room_number'] = int(request.POST['room_number'])
                except Exception:
                    request.session['room_numbers'] = ''
                request.session['category'] = form.cleaned_data.get("category")
                str_capacity = form.cleaned_data.get("capacity")
                # using list comprehension to
                # perform conversion
                try:
                    request.session['capacity'] = [int(i) for i in str_capacity]
                except Exception:
                    request.session['capacity'] = None
                request.session['available_from'] = request.POST['available_from']
                request.session['available_till'] = request.POST['available_till']
                try:
                    request.session['advance'] = int(request.POST['advance'])
                except Exception:
                    request.session['advance'] = None
                #print(request.POST['room_numbers'])
                response = manager_room_search(request.session['room_numbers'],
                                        request.session['category'],
                                        request.session['capacity'],
                                        request.session['available_from'],
                                        request.session['available_till'],
                                        request.session['advance'],
                                        request.user.username)
                #if response:
                context = {
                    'form': form,
                    'rooms': response,
                    'username': request.user.username
                    }
                return render(request, 'manage_rooms.html', context)
                #return HttpResponse("Not Available")
            else:
                context = {
                    'form': form,
                    'time_slots': TimeSlot.objects.filter(room_id=room_number, room_manager=request.user.username),
                    'username': request.user.username
                    }
                return render(request, 'manage_rooms.html', context)
        context = {
                'form': ManageViewTimeSlotForm(),
                #'room_number': room_number,
                'time_slots': TimeSlot.objects.filter(room_manager=request.user.username),
                'username': request.user.username
                }
        return render(request, 'view_time_slots.html', context)
    else:
        return redirect('../book/')

"""Function to delete room."""
@login_required(login_url="/hotel/signin/")
def delete_rooms(request, room_number=None):
    if request.user.email.endswith("@anshul.com"):
        if room_number:
            try:
                room = Room.objects.get(Q(room_number=room_number) & Q(room_manager=request.user.username))
            except Exception:
                return HttpResponse("Not found.")
            room.delete()
            # Implemented Post/Redirect/Get.
            return redirect('../../manage_rooms/')
        else:
            return HttpResponse("Not found.")
    else:
        return redirect('../book/')

"""Function that returns the list of bookings based on the search criteria."""
def manager_book_search(
        str_room_numbers, customer_name, str_check_in_date, str_check_in_time, str_check_out_time, category, person, no_of_rooms, room_manager):

    booking_list = Booking.objects.none()
    spaces_room_numbers = list(str_room_numbers.split(","))
    room_numbers = list()
    for i in spaces_room_numbers:
        room_numbers.append(i.strip())
    check_in_date = convert_to_date(str_check_in_date)
    check_in_time = convert_to_time(str_check_in_time)
    check_out_time = convert_to_time(str_check_out_time)
    for room_number in room_numbers:
        room_number_regex = rf"\b{room_number}\b"
        '''keys = ['room_numbers__iregex', 'customer_name', 'check_in_date', 'check_in_time__gte', 'check_out_time__lte', 'category__in', 'person__in', 'no_of_rooms', 'room_managers__regex']
        values = [room_number_regex, customer_name, check_in_date, check_in_time, check_out_time, category, person, no_of_rooms, room_manager_regex]'''
        keys = ['room_numbers__iregex', 'customer_name', 'check_in_date', 'check_in_time__gte', 'check_out_time__lte', 'category__in', 'person__in', 'no_of_rooms', 'room_managers__regex']
        values = [room_number_regex, customer_name, check_in_date, check_in_time, check_out_time, category, person, no_of_rooms]
        parameters = {}
        for key, value in zip(keys, values):
            if value is not None and value !=[] and value != '':
                parameters[key] = value
        booking_list = Booking.objects.filter(**parameters).union(booking_list).order_by('-check_in_date', 'check_in_time')
    return booking_list

"""Function to display bookings based on the selected criteria."""
@login_required(login_url="/hotel/signin/")
def manage_bookings(request):
    if request.user.email.endswith("@anshul.com"):
        bookings = Booking.objects.filter(room_manager=request.user.username)
        if request.method == 'POST':
            form = ManageBookingForm(request.POST)
            if form.is_valid():
                request.session['room_numbers'] = request.POST['room_numbers']
                #print(request.session['room_numbers'])
                request.session['customer_name'] = request.POST['customer_name']
                try:
                    request.session['check_in_date_month'] = request.POST['check_in_date_month']
                    request.session['check_in_date_day'] = request.POST['check_in_date_day']
                    request.session['check_in_date_year'] = request.POST['check_in_date_year']
                    str_check_in_date = request.session['check_in_date_year'] + '-' + request.session['check_in_date_month'] + '-' + request.session['check_in_date_day']
                except Exception:
                    str_check_in_date = None
                try:
                    request.session['check_in_time'] = request.POST['check_in_time']
                except Exception:
                    request.session['check_in_time'] = None
                try:
                    request.session['check_out_time'] = request.POST['check_out_time']
                except Exception:
                    request.session['check_out_time'] = None
                request.session['category'] = form.cleaned_data.get("category")
                str_person = form.cleaned_data.get("person")
                # using list comprehension to
                # perform conversion
                try:
                    request.session['person'] = [int(i) for i in str_person]
                except Exception:
                    request.session['person'] = None
                try:
                    request.session['no_of_rooms'] = int(request.POST['no_of_rooms'])
                except Exception:
                    request.session['no_of_rooms'] = None
                response = manager_book_search(request.session['room_numbers'],
                                        request.session['customer_name'],
                                        str_check_in_date,
                                        request.session['check_in_time'],
                                        request.session['check_out_time'],
                                        request.session['category'],
                                        request.session['person'],
                                        request.session['no_of_rooms'],
                                        request.user.username)
                context = {
                    'form': form,
                    'bookings': response,
                    'username': request.user.username
                    }
                return render(request, 'manage_bookings.html', context)
            else:
                context = {
                    'form': form,
                    'bookings': bookings,
                    'username': request.user.username
                    }
                return render(request, 'manage_bookings.html', context)
        context = {
                'form': ManageBookingForm(),
                'bookings': bookings,
                'username': request.user.username
                }
        return render(request, 'manage_bookings.html', context)
    else:
        return redirect('../book/')

"""Function for log out."""
def logout_view(request):
    logout(request)
    return redirect('../signin/')

"""Function that returns the list of available categories."""
def search_availability(
        book_date_str, check_in_str, check_out_str,
        person, normal_no_of_rooms_required):
    book_date = convert_to_date(book_date_str)
    check_in = convert_to_time(check_in_str)
    check_out = convert_to_time(check_out_str)
    normal_regular_rooms = 0
    normal_executive_rooms = 0
    normal_deluxe_rooms = 0
    normal_king_rooms = 0
    normal_queen_rooms = 0
    available_categories = list()
    room_list = Room.objects.filter(
        available_from__lte=check_in,
        available_till__gte=check_out,
        capacity__gte=person
    )
    for room in room_list:
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + datetime.timedelta(days=room.advance)
        if (book_date <= max_book.date()):
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
            # Checking if the room is already booked.
            taken = Booking.objects.filter(Q(Q(check_in_time__lt=added_check_out)
                                             | Q(check_out_time__gt=subtracted_check_in))
                                           & Q(room_numbers__contains=room.room_number)
                                           & Q(check_in_date=book_date))
            if not taken:
                if (room.category == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                elif (room.category == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                elif (room.category == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                elif (room.category == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                elif (room.category == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
                if (normal_regular_rooms == normal_no_of_rooms_required and room.category == 'Regular'):
                    available_categories.append('Regular')
                if (normal_executive_rooms == normal_no_of_rooms_required and room.category == 'Executive'):
                    available_categories.append('Executive')
                if (normal_deluxe_rooms == normal_no_of_rooms_required and room.category == 'Deluxe'):
                    available_categories.append('Deluxe')
                if (normal_king_rooms == normal_no_of_rooms_required and room.category == 'King'):
                    available_categories.append('King')
                if (normal_queen_rooms == normal_no_of_rooms_required and room.category == 'Queen'):
                    available_categories.append('Queen')
    return available_categories

"""Function to return the available categories."""
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            request.session['normal_book_date'] = request.POST['check_in_date']
            request.session['normal_check_in'] = request.POST['check_in_time']
            request.session['normal_check_out'] = request.POST['check_out_time']
            request.session['normal_person'] = int(request.POST['person'])
            request.session['normal_no_of_rooms_required'] = int(
                request.POST['no_of_rooms']
                )
            response = search_availability(request.session['normal_book_date'],
                                           request.session['normal_check_in'],
                                           request.session['normal_check_out'],
                                           request.session['normal_person'],
                                           request.session['normal_no_of_rooms_required'])
            #if response:
            context = {
                'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'categories': response,
                'username': request.user.username
                }
            return render(request, 'categories.html', context)
            #return HttpResponse("Not Available")
        else:
            context = {
                'form': form,
                'username': request.user.username
                }
            return render(request, 'book.html', context)
    context = {
        'form': BookingForm(),
        'username': request.user.username
        }
    return render(request, 'book.html', context)

"""Function to book the time slot."""
def time_booking(
        room_numbers, room_type, no_of_rooms_required, normal_username,
        normal_book_date, normal_check_in, normal_check_out, normal_person, room_managers):
    #for i in range(no_of_rooms_required):
        #room_no = room_numbers.pop()
    #print(room_numbers)


    # getting the comma-separated string from the list
    room_numbers_string = ", ".join([str(item) for item in room_numbers if item])
    room_managers_string = ", ".join([str(item) for item in room_managers if item])

    time_slot = Booking(customer_name=normal_username,
                        check_in_date=normal_book_date,
                        check_in_time=normal_check_in,
                        check_out_time=normal_check_out,
                        room_numbers=room_numbers_string,
                        category=room_type, person=normal_person,
                        no_of_rooms = no_of_rooms_required,
                        room_managers=room_managers_string)
    time_slot.save()

"""Function to check if the room(s) is/are available."""
def room_category(
        room_type, normal_username, normal_book_date_str,normal_check_in_str,
        normal_check_out_str, normal_person, normal_no_of_rooms_required):
    normal_book_date = convert_to_date(normal_book_date_str)
    normal_check_in = convert_to_time(normal_check_in_str)
    normal_check_out = convert_to_time(normal_check_out_str)
    normal_regular_rooms = 0
    normal_executive_rooms = 0
    normal_deluxe_rooms = 0
    normal_king_rooms = 0
    normal_queen_rooms = 0
    room_numbers = list()
    room_managers = list()
    # List of rooms for the given category.
    try:
        room_list = Room.objects.filter(
            available_from__lte=normal_check_in,
            available_till__gte=normal_check_out,
            capacity__gte=normal_person, category=room_type
        )
    except Exception:
        return 3
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        if (normal_book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = normal_check_out.replace(
                hour=(normal_check_out.hour + 1) % 24
            )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = normal_check_in.replace(
                hour=(normal_check_in.hour - 1) % 24
            )
            taken = Booking.objects.filter(
                Q(Q(check_in_time__lt=added_check_out)
                  | Q(check_out_time__gt=subtracted_check_in))
                & Q(room_numbers__contains=room.room_number)
                & Q(check_in_date=normal_book_date))
            if not taken:
                if (room_type == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                    room_numbers.append(room.room_number)
                    room_managers.append(room.room_manager)
                elif (room_type == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                    room_numbers.append(room.room_number)
                    room_managers.append(room.room_manager)
                elif (room_type == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                    room_numbers.append(room.room_number)
                    room_managers.append(room.room_manager)
                elif (room_type == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                    room_numbers.append(room.room_number)
                    room_managers.append(room.room_manager)
                elif (room_type == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
                    room_numbers.append(room.room_number)
                    room_managers.append(room.room_manager)
                if (room_type == 'Regular' and
                    normal_regular_rooms == normal_no_of_rooms_required  and room.category == 'Regular'):
                    time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                                    normal_username, normal_book_date, normal_check_in,
                                    normal_check_out, normal_person, room_managers)
                    return 1
                elif (room_type == 'Executive' and
                    normal_executive_rooms == normal_no_of_rooms_required and room.category == 'Executive'):
                    time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                                    normal_username, normal_book_date, normal_check_in,
                                    normal_check_out, normal_person)
                    return 1
                elif (room_type == 'Deluxe' and
                    normal_deluxe_rooms == normal_no_of_rooms_required and room.category == 'Deluxe'):
                    time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                                    normal_username, normal_book_date, normal_check_in,
                                    normal_check_out, normal_person)
                    return 1
                elif (room_type == 'King' and
                    normal_king_rooms == normal_no_of_rooms_required and room.category == 'King'):
                    time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                                    normal_username, normal_book_date, normal_check_in,
                                    normal_check_out, normal_person)
                    return 1
                elif (room_type == 'Queen' and
                    normal_queen_rooms == normal_no_of_rooms_required and room.category == 'Queen'):
                    time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                                    normal_username, normal_book_date, normal_check_in,
                                    normal_check_out, normal_person)
                    return 1
    return 2

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def regular(request):
    room_status = room_category('Regular', request.user.username,
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_regular/')
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def executive(request):
    room_status = room_category('Executive',
                                request.user.username,
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_executive/')
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def deluxe(request):
    room_status = room_category('Deluxe', request.user.username,
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_deluxe/')
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def king(request):
    room_status = room_category('King', request.user.username,
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_king/')
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def queen(request):
    room_status = room_category('Queen', request.user.username,
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_queen/')
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/signin/")
def booked_regular(request):
    try:
        context = {'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'category': 'Regular',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/signin/")
def booked_executive(request):
    try:
        context = {'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'category': 'Executive',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/signin/")
def booked_deluxe(request):
    try:
        context = {'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'category': 'Deluxe',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/signin/")
def booked_king(request):
    try:
        context = {'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'category': 'King',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/signin/")
def booked_queen(request):
    try:
        context = {'book_date': request.session['normal_book_date'],
                'check_in': request.session['normal_check_in'],
                'check_out': request.session['normal_check_out'],
                'person': request.session['normal_person'],
                'no_of_rooms_required': request.session['normal_no_of_rooms_required'],
                'category': 'Queen',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to return all the bookings."""
@login_required(login_url="/hotel/signin/")
def all_bookings(request, pk=None):
    if pk:
        try:
            booking = Booking.objects.get(pk=pk)
        except Exception:
            return HttpResponse("Not found.")
        if booking.customer_name == request.user.username:
            booking.delete()
            # Implemented Post/Redirect/Get.
            return redirect('../../all_bookings/')
        else:
            return HttpResponse("Not allowed.")
    # Future bookings.
    future_bookings = Booking.objects.filter(
        customer_name=request.user.username,
        check_in_date__gt=now.date()
    ).order_by('-check_in_date', 'check_in_time')
    # Current and past bookings.
    current_and_past_bookings = Booking.objects.filter(
        customer_name=request.user.username,
        check_in_date__lte=now.date()
    ).order_by('-check_in_date', 'check_in_time')
    context = {
        'future_bookings': future_bookings,
        'current_and_past_bookings': current_and_past_bookings,
        'username': request.user.username
    }
    return render(request, 'all_bookings.html', context)

"""API endpoints for User management, Rooms, Time Slots, and
corresponding Bookings.
"""

@api_view(['GET', 'POST'])
def room_list(request):
    """
    List all rooms, or create a new room.
    """
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def room_detail(request, pk):
    """
    Retrieve, update or delete a room.
    """
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_list(request):
    """
    To register a user.
    """
    if request.method == 'POST':
        serializer = CustomerAPISerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    serializer.validated_data['desired_username'],
                    serializer.validated_data['your_email'],
                    serializer.validated_data['password']
                )
                user.first_name = serializer.validated_data['first_name']
                user.last_name = serializer.validated_data['last_name']
                user.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except Exception:
                return Response(serializer.errors,
                                status=
                                status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Function for viewing profile."""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile = User.objects.filter(
        username=request.user.username
        ).values()
    serializer = CustomerSerializer(profile, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    """
    List all bookings, or create a new booking.
    """
    request.session['api_username'] = request.user.username
    if request.method == 'GET':
        if request.user.is_active and request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-check_in_date', 'check_in_time')
            serializer = BookingSerializerAdmin(bookings, many=True)
            return Response(serializer.data)
        bookings = Booking.objects.filter(
                                            customer_name=request.session['api_username']
                                         ).order_by('-check_in_date', 'check_in_time')
        for boo in bookings:
            print(boo.check_in_time)
        serializer = BookingSerializerGet(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_active and request.user.is_superuser:
            serializer = BookingSerializerAdminWithoutid(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingSerializerBook(data=request.data)
        if serializer.is_valid():
            request.session['api_book_date'] = str(serializer.validated_data['check_in_date'])
            request.session['api_check_in'] = str(serializer.validated_data['check_in_time'])
            request.session['api_check_out'] = str(serializer.validated_data['check_out_time'])
            request.session['api_person'] = serializer.validated_data['person']
            request.session['no_of_rooms'] = serializer.validated_data['no_of_rooms']
            print(request.session['api_check_in'])
            response = search_availability(request.session['api_book_date'], request.session['api_check_in'], request.session['api_check_out'], request.session['api_person'], request.session['no_of_rooms'])
            if response:
                context = {'categories': response}

            else:
                context = dict()
            return Response(context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_category(request, category):
    """
    To book a room for a given category.
    """
    normal_regular_rooms = 0
    normal_executive_rooms = 0
    normal_deluxe_rooms = 0
    normal_king_rooms = 0
    normal_queen_rooms = 0
    room_numbers = list()
    # List of rooms for the given category.
    try:
        room_list = Room.objects.filter(
            available_from__lte=request.session['api_check_in'],
            available_till__gte=request.session['api_check_out'],
            capacity__gte=request.session['api_person'], category=category
        )
    except Exception:
        return Response({'msg': 'No such category exist.'},
                        status=status.HTTP_400_BAD_REQUEST)
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        # Ensuring that books are book before a room max advance
        if (request.session['api_book_date'] <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = request.session['api_check_out'].replace(
                hour=(request.session['api_check_out'].hour + 1) % 24
            )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = request.session['api_check_in'].replace(
                hour=(request.session['api_check_in'].hour - 1) % 24
            )
            taken = Booking.objects.filter(
                Q(Q(check_in_time__lt=added_check_out)
                  | Q(check_out_time__gt=subtracted_check_in))
                & Q(room_numbers__contains=room.room_number)
                & Q(check_in_date=request.session['api_book_date']))
            if not taken:
                if (category == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                    room_numbers.append(room.room_number)
                elif (category == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                    room_numbers.append(room.room_number)
                elif (category == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                    room_numbers.append(room.room_number)
                elif (category == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                    room_numbers.append(room.room_number)
                elif (category == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
                    room_numbers.append(room.room_number)
                if (category == 'Regular' and
                    normal_regular_rooms == request.session['no_of_rooms']):
                    time_booking(room_numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Executive' and
                    normal_executive_rooms == request.session['no_of_rooms']):
                    time_booking(room_numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Deluxe' and
                    normal_deluxe_rooms == request.session['no_of_rooms']):
                    time_booking(room_numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'King' and
                    normal_king_rooms == request.session['no_of_rooms']):
                    time_booking(room_numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Queen' and
                    normal_queen_rooms == request.session['no_of_rooms']):
                    time_booking(room_numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
    return Response({'msg': 'Unavailable.'})

    '''            time_slot = Booking(
                    customer_name=request.session['api_username'],
                    check_in_date=request.session['api_book_date'],
                    check_in_time=request.session['api_check_in'],
                    check_out_time=request.session['api_check_out'],
                    room_number=room.room_number,
                    category=category, person=request.session['api_person'], no_of_rooms=request.session['no_of_rooms']
                )
                time_slot.save()

                request.session['api_username'] = None
                request.session['api_book_date'] = None
                request.session['api_check_in'] = None
                request.session['api_check_out'] = None
                category = None
                request.session['api_person'] = None
                return Response({'msg': 'Booked'})
        return Response({'msg': 'Unavailable.'},
                        status=status.HTTP_404_NOT_FOUND)
    request.session['api_username'] = None
    request.session['api_book_date'] = None
    request.session['api_check_in'] = None
    request.session['api_check_out'] = None
    category = None
    request.session['api_person'] = None
    return Response({'msg': 'Unavailable'}, status=status.HTTP_404_NOT_FOUND)'''

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_detail(request, pk, format=None):
    """
    Retrieve, update or delete a booking.
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response({'msg': 'Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    # To get the user name from the request body.
    obj = Booking.objects.first()
    field_value = getattr(obj, 'customer_name')
    if request.user.is_active and request.user.is_superuser:
        if request.method == 'GET':
            serializer = BookingSerializerAdminWithoutid(booking)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BookingSerializerAdminWithoutid(booking, 
                                                            data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    # To check if it is a normal user checking the booking details of 
    # his/her room.
    elif request.user.username == field_value:
        # To get book from date from the request body.
        field_value2 = getattr(obj, 'check_in_date')
        # To check if the deleted booking is for future.
        if (field_value2 > now.date()):
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'msg': 'Past booking'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    else:
        return Response({'msg': 'Not allowed'},
                        status=status.HTTP_403_FORBIDDEN)
