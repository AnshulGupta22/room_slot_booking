from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#import datetime
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from hotel.forms import CustomerForm, SignInForm, BookingForm, RoomsForm, ManageBookingForm, AddRoomForm, ManageViewTimeSlotForm, SearchTimeSlotsForm, AddTimeSlotForm, EditRoomForm, EditForm
from .models import Room, Booking, TimeSlot

from .serializers import (
    RoomSerializer, BookingSerializerBook, BookingSerializerAdmin,
    BookingSerializerGet, BookingSerializerAdminWithoutid,
    CustomerAPISerializer, CustomerSerializer
    )

# Create your views here.

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
                return redirect('../rooms/')
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'sign_in.html', context)
    context = {'form': SignInForm()}
    return render(request, 'sign_in.html', context)

"""Function for viewing profile."""
@login_required(login_url="/hotel/sign_in/")
def view_profile(request):
    profile = User.objects.filter(
        username=request.user.username
        ).values()
    context = {'profile': profile}
    return render(request, 'view_profile.html', context)

"""Function for editing profile."""
@login_required(login_url="/hotel/sign_in/")
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

"""Function for logout."""
def logout_view(request):
    logout(request)
    return redirect('../sign_in/')

"""Function that returns the list of rooms based on the search criterias."""
def rooms_search(
        str_numbers, categories, capacities, advance, manager, sort_by):
    if str_numbers != '':
        spaces_numbers = list(str_numbers.split(","))
        numbers = list()
        for i in spaces_numbers:
            numbers.append(i.strip())
    else:
        numbers = ''
    keys = ['number__in', 'category__in', 'capacity__in', 'advance__gte', 'manager']
    values = [numbers, categories, capacities, advance, manager]
    parameters = {}
    for key, value in zip(keys, values):
        if value is not None and value !=[] and value != '':
            parameters[key] = value
    room_list = Room.objects.filter(**parameters).order_by(sort_by)
    return room_list

"""Function to display rooms based on the selected criterias."""
@login_required(login_url="/hotel/sign_in/")
def rooms(request):
    if request.user.email.endswith("@anshul.com"):
        #rooms = Room.objects.filter(manager=request.user)
        rooms = Room.objects.filter(manager=request.user)
        if request.method == 'POST':
            form = RoomsForm(request.POST)
            if form.is_valid():
                try:
                    request.session['numbers'] = request.POST['numbers']
                except Exception:
                    request.session['numbers'] = ''
                request.session['categories'] = form.cleaned_data.get("categories")
                str_capacity = form.cleaned_data.get("capacities")
                # using list comprehension to perform conversion
                try:
                    request.session['capacities'] = [int(i) for i in str_capacity]
                except Exception:
                    request.session['capacities'] = None
                try:
                    request.session['advance'] = int(request.POST['advance'])
                except Exception:
                    request.session['advance'] = None
                response = rooms_search(request.session['numbers'],
                                        request.session['categories'],
                                        request.session['capacities'],
                                        request.session['advance'],
                                        request.user,
                                        request.POST['sort_by'])
                context = {
                    'form': form,
                    'rooms': response,
                    'username': request.user.username
                    }
                return render(request, 'rooms.html', context)
            else:
                context = {
                    'form': form,
                    'rooms': None,
                    'username': request.user.username
                    }
                return render(request, 'rooms.html', context)
        context = {
                'form': RoomsForm(),
                'rooms': rooms,
                'username': request.user.username
                }
        return render(request, 'rooms.html', context)
    else:
        return redirect('../book/')

"""Function to add a room."""
@login_required(login_url="/hotel/sign_in/")
def add_room(request):
    if request.user.email.endswith("@anshul.com"):
        if request.method == 'POST':
            form = AddRoomForm(request.POST)
            if form.is_valid():
                '''room = Room(number=request.POST['number'],
                        category=request.POST['category'],
                        capacity=request.POST['capacity'],
                        advance=request.POST['advance'],
                        manager=request.user)
                room.save()'''

                form.instance.manager = request.user
                form.save()
                # Implemented Post/Redirect/Get.
                return redirect('../rooms/')
            else:
                context = {
                    'form': form,
                    'username': request.user.username
                    }
                return render(request, 'add_room.html', context)
        context = {
                'form': AddRoomForm(),
                'username': request.user.username
                }
        return render(request, 'add_room.html', context)
    else:
        return redirect('../book/')

"""Function to edit a room."""
@login_required(login_url="/hotel/sign_in/")
def edit_room(request, number):
    if request.user.email.endswith("@anshul.com"):
        try:
            room = Room.objects.get(number=number, manager=request.user)
        except Exception:
            return HttpResponse("Not Found.")
        if request.method == 'POST':
            form = EditRoomForm(request.POST, instance=room)
            if form.is_valid():
                '''room = Room(number=request.POST['number'],
                        category=request.POST['category'],
                        capacity=request.POST['capacity'],
                        advance=request.POST['advance'],
                        manager=request.user)
                room.save()'''

                form.instance.manager = request.user
                form.save()

                # Implemented Post/Redirect/Get.
                if number:
                    return redirect('../../rooms/')
            else:
                context = {
                    'form': form,
                    'number': number,
                    'username': request.user.username
                    }
                return render(request, 'edit_room.html', context)
        context = {
                'form': EditRoomForm(instance=room),
                'number': number,
                'username': request.user.username
                }
        return render(request, 'edit_room.html', context)
    else:
        return redirect('../book/')

"""Function to delete room."""
@login_required(login_url="/hotel/sign_in/")
def delete_rooms(request, number):
    if request.user.email.endswith("@anshul.com"):
        try:
            room = Room.objects.get(Q(number=number) & Q(manager=request.user))
        except Exception:
            return HttpResponse("Not Found.")
        room.delete()
        return redirect('../../rooms/')
    else:
        return redirect('../book/')

# """Function to convert string to time."""
# def convert_to_time(date_time):
#     format = '%H:%M'
#     try:
#         datetime_str = datetime.datetime.strptime(date_time, format).time()
#     except Exception:
#         datetime_str = None
#     return datetime_str


# """Function to convert string to time."""
# def convert_to_time(date_time):
#     return datetime.datetime.strptime(date_time, '%H:%M').time()





"""Function that returns the list of rooms based on the search criteria."""
def time_slots_search(
        number, date, str_available_from, str_available_till, occupancy, sort_by):
    room_obj = Room.objects.get(number=number)
    '''if str_numbers != '':
        spaces_numbers = list(str_numbers.split(","))
        numbers = list()
        for i in spaces_numbers:
            numbers.append(i.strip())
    else:
        numbers = '''''
    available_from = ''
    available_till = ''
    if str_available_from != '':
        available_from = datetime.strptime(str_available_from, '%H:%M').time() #Function to convert string to time.
        available_till = datetime.strptime(str_available_till, '%H:%M').time() #Function to convert string to time.

    # if available_from is None or available_till is None:
    #     return None
    #print(available_from)
    #room_list = list()
    #for category in categories:
    '''room_list = Room.objects.filter(
        number=number,
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
    #print(occupancies)
    '''keys = ['room_number__in', 'category__in', 'available_from__lte', 'available_till__gte', 'capacity__in', 'advance__gte', 'manager']
    values = [numbers, categories, available_from, available_till, capacities, advance, username]'''
    # if available_from is None:
    #     keys = ['room', 'available_from__lt', 'available_till__gte', 'occupancy']
    #     values = [room_obj, available_till, available_till, occupancies]
    # elif available_till is None:
    #     keys = ['room', 'available_from__lte', 'available_till__gt', 'occupancy']
    #     values = [room_obj, available_from, available_from, occupancies]
    # else:
    #     keys = ['room', 'available_from__lte', 'available_till__gte', 'occupancy']
    #     values = [room_obj, available_from, available_till, occupancies]

    # keys = ['room', 'available_from__lte', 'available_till__gte', 'occupancy']
    # values = [room_obj, available_from, available_till, occupancy]

    keys = ['room', 'available_from__lte', 'available_till__gte', 'occupancy']
    values = [room_obj, available_from, available_till, occupancy]

    parameters = {}
    #temp = {'category__in': categories, 'available_from__lte': available_from, 'available_till__gte': available_till, 'capacity__in': capacities, 'advance__gte': advance}

    for key, value in zip(keys, values):
        if value != '':
            parameters[key] = value
    #for key, value in temp:available_till__gte
    #    if value is not None and value !=[]:
    #        parameters[key] = value
    #print(parameters)

    time_slots_list = TimeSlot.objects.filter(**parameters).order_by(sort_by)

    #time_slots_list = TimeSlot.objects.filter(room=room_obj, available_from__lte=available_from, available_till__gte=available_till, occupancy=occupancy)

    '''room_list = Room.objects.filter(
        category__in=categories,
        available_from__lte=available_from,
        available_till__gte=available_till,
        capacity__in=capacities,
        advance__gte=advance
    )'''
    #print(time_slots_list)
    return time_slots_list
        #select * from ROOM where db_room_number = number and db_category IN category and db_capacity IN capacity and db_available_from <= available_from and db_available_till >= available_till and db_advance >= advance
    """print(room_list)
    for capacity in capacities:
        room_list += Room.objects.filter(
            number=number,
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
            # before check-in.
            subtracted_check_in = check_in.replace(
                hour=(check_in.hour - 1) % 24
            )
            # Checking if the room is already booked.
            taken = Booking.objects.filter(Q(Q(check_in_time__lt=added_check_out)
                                             | Q(check_out_time__gt=subtracted_check_in))
                                           & Q(room_number__contains=room.number)
                                           & Q(check_in_date=book_date))
            if not taken:
                if (room.category == 'Regular'):
                    regular_rooms = regular_rooms + 1
                elif (room.category == 'Executive'):
                    executive_rooms = executive_rooms + 1
                elif (room.category == 'Deluxe'):
                    deluxe_rooms = deluxe_rooms + 1
                elif (room.category == 'King'):
                    king_rooms = king_rooms + 1
                elif (room.category == 'Queen'):
                    queen_rooms = queen_rooms + 1
    if (regular_rooms >= no_of_rooms_required):
        available_categories.append('Regular')
    if (executive_rooms >= no_of_rooms_required):
        available_categories.append('Executive')
    if (deluxe_rooms >= no_of_rooms_required):
        available_categories.append('Deluxe')
    if (king_rooms >= no_of_rooms_required):
        available_categories.append('King')
    if (queen_rooms >= no_of_rooms_required):
        available_categories.append('Queen')
    return available_categories"""

"""Function to search time slots."""
@login_required(login_url="/hotel/sign_in/")
def time_slots(request, number):
    if request.user.email.endswith("@anshul.com"):
        try:
            room = Room.objects.get(number=number, manager=request.user)
        except Exception:
            return HttpResponse("Not Found.")
        if request.method == 'POST':
            form = SearchTimeSlotsForm(request.POST)
            if form.is_valid():
                #print(form.cleaned_data.get("booked"))
                #request.session['booked'] = form.cleaned_data.get("booked")
                '''booked = True
                try:
                    request.POST['booked']
                except Exception:
                    booked = False'''
                '''try:
                    request.session['numbers'] = request.POST['numbers']
                    #print(request.session['numbers'])
                    #request.session['number'] = int(request.POST['number'])
                except Exception:
                    request.session['numbers'] = ''
                request.session['category'] = form.cleaned_data.get("category")
                str_capacity = form.cleaned_data.get("capacity")
                # using list comprehension to
                # perform conversion
                try:
                    request.session['capacity'] = [int(i) for i in str_capacity]
                except Exception:
                    request.session['capacity'] = None'''
                request.session['date'] = request.POST['date']
                request.session['available_from'] = request.POST['available_from']
                request.session['available_till'] = request.POST['available_till']
                request.session['occupancy'] = form.cleaned_data.get("occupancy")

                '''try:
                    request.session['advance'] = int(request.POST['advance'])
                except Exception:
                    request.session['advance'] = None'''

                time_slots = time_slots_search(number,
                                        request.session['date'],
                                        request.session['available_from'],
                                        request.session['available_till'], request.session['occupancy'], request.POST['sort_by']
                                        )
                #if response:
                #print(time_slots)
                context = {
                    'form': form,
                    'room': room,
                    'time_slots': time_slots,
                    'username': request.user.username
                    }
                return render(request, 'time_slots.html', context)
                #return HttpResponse("Not Available")
            else:
                context = {
                    'form': form,
                    'room': room,
                    'time_slots': None,
                    'username': request.user.username
                    }
                return render(request, 'time_slots.html', context)
        context = {
                'form': SearchTimeSlotsForm(),
                'room': room,
                #'number': number,
                #'time_slots': TimeSlot.objects.filter(room=number, manager=request.user),
                'time_slots': TimeSlot.objects.filter(room_id=number),
                'username': request.user.username
                }
        return render(request, 'time_slots.html', context)
    else:
        return redirect('../book/')

"""Function to add time slot."""
@login_required(login_url="/hotel/sign_in/")
def add_time_slot(request, number):
    if request.user.email.endswith("@anshul.com"):
        if request.method == 'POST':
            form = AddTimeSlotForm(request.POST)
            if form.is_valid():
                try:
                    room_obj = Room.objects.get(number=number, manager=request.user)
                except Exception:
                    return HttpResponse("Not Found.")

                available_till = datetime.strptime(request.POST['available_till'], '%H:%M').time() #Function to convert string to time.
                available_from = datetime.strptime(request.POST['available_from'], '%H:%M').time() #Function to convert string to time.

                # To ensure no rooms are booked within a gap of 1 hour
                # after checkout.
                added_available_till = available_till.replace(
                    hour=(available_till.hour + 1) % 24
                )

                # To ensure no rooms are booked within a gap of 1 hour
                # before check-in.
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
                    '''time_slot = TimeSlot(room=room_obj,
                            available_from=available_from,
                            available_till=available_till)
                    time_slot.save()'''

                    form.instance.room = room_obj
                    form.save()

                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../time_slots/{room_obj.number}/')
                else:
                    return HttpResponse("Time slot not available.")
            else:
                context = {
                    'form': form,
                    'number': number,
                    'username': request.user.username
                    }
                return render(request, 'add_time_slot.html', context)
        context = {
                'form': AddTimeSlotForm(),
                'number': number,
                'username': request.user.username
                }
        return render(request, 'add_time_slot.html', context)
    else:
        return redirect('../book/')

"""Function to convert string to time."""
def convert_to_time_sec(date_time):
    format = '%H:%M:%S'
    try:
        datetime_str = datetime.strptime(date_time, format).time()
    except Exception:
        datetime_str = None
    return datetime_str

"""Function to edit time slot."""
@login_required(login_url="/hotel/sign_in/")
def edit_time_slot(request, pk):
    if request.user.email.endswith("@anshul.com"):
        try:
            #time_slot_obj = TimeSlot.objects.get(pk=pk)
            time_slot_obj = TimeSlot.objects.get(Q(pk=pk) & Q(occupancy='Vacant'))
        except Exception:
            return HttpResponse("Not Found.")

        if str(time_slot_obj.room.manager) != request.user.username:
            return HttpResponse("Not Found.")
        #if time_slot_obj.occupancy == 'Booked':
            #return HttpResponse("Bad request.")
        if request.method == 'POST':
            form = AddTimeSlotForm(request.POST, instance=time_slot_obj)
            if form.is_valid():
                try:
                    Room.objects.get(number=time_slot_obj.room.number, manager=request.user)
                except Exception:
                    return HttpResponse("Not Found.")
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
                # before check-in.
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
                    return redirect(f'../../time_slots/{time_slot_obj.room.number}/')
                else:
                    if taken.count() == 1:
                        for record in taken:
                            # Checking if the new time slot is a smaller version of the existing time slot. For e.g. if the existing time slot is from 1:00 to 8:00 and we are changing it to 4:00 to 5:00.
                            if record.pk == time_slot_obj.pk and time_slot_obj.available_from <= available_from and time_slot_obj.available_till >= available_till:
                                time_slot_obj.available_from = available_from
                                time_slot_obj.available_till = available_till
                                time_slot_obj.save()
                                # Implemented Post/Redirect/Get.
                                return redirect(f'../../time_slots/{time_slot_obj.room.number}/')
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
                    return redirect(f'../../time_slots/{time_slot_obj.room.number}/')
                    elif record.pk == time_slot_obj.pk and time_slot_obj.available_from <= available_from and time_slot_obj.available_till >= available_till:
                    time_slot_obj.available_from = available_from
                    time_slot_obj.available_till = available_till
                    time_slot_obj.save()
                    # Implemented Post/Redirect/Get.
                    return redirect(f'../../time_slots/{time_slot_obj.room.number}/')'''                
            else:
                context = {
                    'form': form,
                    'username': request.user.username,
                    'number': time_slot_obj.room.number
                    }
                return render(request, 'add_time_slot.html', context)
        context = {
                'form': AddTimeSlotForm(instance=time_slot_obj),
                'username': request.user.username,
                'number': time_slot_obj.room.number
                }
        return render(request, 'edit_time_slot.html', context)
    else:
        return redirect('../book/')

"""Function to delete time slot."""
@login_required(login_url="/hotel/sign_in/")
def delete_time_slot(request, pk):
    if request.user.email.endswith("@anshul.com"):
        try:
            time_slot_obj = TimeSlot.objects.get(Q(pk=pk) & Q(occupancy='Vacant'))
        except Exception:
            return HttpResponse("Not Found.")
        if str(time_slot_obj.room.manager) != request.user.username:
            return HttpResponse("Not Found.")
        time_slot_obj.delete()
        # Implemented Post/Redirect/Get.
        return redirect(f'../../time_slots/{time_slot_obj.room.number}/')
    else:
        return redirect('../book/')

"""Function that returns the list of available categories."""
def search_availability(
        book_date_str, check_in_str, check_out_str,
        person, no_of_rooms_required):
    #book_date = convert_to_date(book_date_str)

    # Converting string to date.
    book_date = datetime.strptime(book_date_str, '%Y-%m-%d').date()
    check_in = datetime.strptime(check_in_str, '%H:%M').time()
    check_out = datetime.strptime(check_out_str, '%H:%M').time()

    room_list = Room.objects.filter(
        capacity__gte=person
    ).order_by('capacity')
    regular_rooms = 0
    executive_rooms = 0
    deluxe_rooms = 0
    available_categories = list()
    #time_slots = TimeSlot.objects.none()
    for room in room_list:
        
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + timedelta(days=room.advance)
        if (book_date <= max_book.date()):
            try:
                # time_slots = TimeSlot.objects.get(
                #     room=room,
                #     available_from_lte=check_in,
                #     available_till_gte=check_out,
                # ).union(time_slots)

                time_slot = TimeSlot.objects.get(
                    room=room,
                    available_from__lte=check_in,
                    available_till__gte=check_out,
                )
            except Exception:
                continue
            try:
                #taken = Booking.objects.get(Q(time_slot_ids__contains=time_slot.id)
                #                            & Q(check_in_date=book_date))
                Booking.objects.get(Q(time_slot_ids__contains=time_slot.id)
                                            & Q(check_in_date=book_date))
            except Exception:
            #if not taken:
                if (time_slot.room.category == 'Regular'):
                    regular_rooms = regular_rooms + 1
                elif (time_slot.room.category == 'Executive'):
                    executive_rooms = executive_rooms + 1
                elif (time_slot.room.category == 'Deluxe'):
                    deluxe_rooms = deluxe_rooms + 1

                if (regular_rooms == no_of_rooms_required and time_slot.room.category == 'Regular'):
                    available_categories.append('Regular')
                if (executive_rooms == no_of_rooms_required and time_slot.room.category == 'Executive'):
                    available_categories.append('Executive')
                if (deluxe_rooms == no_of_rooms_required and time_slot.room.category == 'Deluxe'):
                    available_categories.append('Deluxe')
    return available_categories

            # if not taken:
            #     time_slots = time_slots.union(time_slot)
                
            


            

            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            # added_check_out = check_out.replace(
            #     hour=(check_out.hour + 1) % 24
            # )
            # To ensure no rooms are booked within a gap of 1 hour
            # before check-in.
            # subtracted_check_in = check_in.replace(
            #     hour=(check_in.hour - 1) % 24
            # )
            # Checking if the room is already booked.
            # taken = Booking.objects.filter(Q(Q(check_in_time__lt=added_check_out)
            #                                  | Q(check_out_time__gt=subtracted_check_in))
            #                                & Q(room_numbers__contains=room.number)
            #                                & Q(check_in_date=book_date))
            # if not taken:
            #     if (room.category == 'Regular'):
            #         regular_rooms = regular_rooms + 1
            #     elif (room.category == 'Executive'):
            #         executive_rooms = executive_rooms + 1
            #     elif (room.category == 'Deluxe'):
            #         deluxe_rooms = deluxe_rooms + 1
            #     elif (room.category == 'King'):
            #         king_rooms = king_rooms + 1
            #     elif (room.category == 'Queen'):
            #         queen_rooms = queen_rooms + 1
            #     if (regular_rooms == no_of_rooms_required and room.category == 'Regular'):
            #         available_categories.append('Regular')
            #     if (executive_rooms == no_of_rooms_required and room.category == 'Executive'):
            #         available_categories.append('Executive')
            #     if (deluxe_rooms == no_of_rooms_required and room.category == 'Deluxe'):
            #         available_categories.append('Deluxe')
            #     if (king_rooms == no_of_rooms_required and room.category == 'King'):
            #         available_categories.append('King')
            #     if (queen_rooms == no_of_rooms_required and room.category == 'Queen'):
            #         available_categories.append('Queen')
    #return available_categories






# regular_rooms = 0
#     executive_rooms = 0
#     deluxe_rooms = 0
#     king_rooms = 0
#     queen_rooms = 0
#     available_categories = list()
#     room_list = Room.objects.filter(
#         available_from__lte=check_in,
#         available_till__gte=check_out,
#         capacity__gte=person
#     )

"""Function for booking."""
@login_required(login_url="/hotel/sign_in/")
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            request.session['book_date'] = request.POST['check_in_date']
            request.session['check_in'] = request.POST['check_in_time']
            request.session['check_out'] = request.POST['check_out_time']
            request.session['person'] = int(request.POST['person'])
            request.session['no_of_rooms_required'] = int(
                request.POST['no_of_rooms']
                )
            response = search_availability(request.session['book_date'],
                                           request.session['check_in'],
                                           request.session['check_out'],
                                           request.session['person'],
                                           request.session['no_of_rooms_required'])
            #if response:
            context = {
                'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
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

now = timezone.now()

"""Function to convert string to date."""
# def convert_to_date(date_time):
#     format = '%Y-%m-%d'
#     try:
#         datetime_str = datetime.datetime.strptime(date_time, format).date()

#         datetime.datetime.strptime(date_time, '%Y-%m-%d').date()
#     except Exception:
#         datetime_str = None
#     return datetime_str

"""Function to add/ edit time_slot."""
@login_required(login_url="/hotel/sign_in/")
def manage_time_slots(request):
    if request.user.email.endswith("@anshul.com"):
        '''if number:
            time_slot = TimeSlot.objects.get(number=number)
        else:
            time_slot = TimeSlot()'''
        asd = TimeSlot.objects.all()
        for course in asd:
            print(getattr(course, 'category'))
        if request.method == 'POST':
            form = ManageViewTimeSlotForm(request.POST)
            if form.is_valid():
                try:
                    request.session['numbers'] = request.POST['numbers']
                    #print(request.session['numbers'])
                    #request.session['number'] = int(request.POST['number'])
                except Exception:
                    request.session['numbers'] = ''
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
                #print(request.POST['numbers'])
                response = rooms_search(request.session['numbers'],
                                        request.session['category'],
                                        request.session['capacity'],
                                        request.session['available_from'],
                                        request.session['available_till'],
                                        request.session['advance'],
                                        request.user)
                #if response:
                context = {
                    'form': form,
                    'rooms': response,
                    'username': request.user.username
                    }
                return render(request, 'rooms.html', context)
                #return HttpResponse("Not Available")
            else:
                context = {
                    'form': form,
                    'time_slots': TimeSlot.objects.filter(room_id=number, manager=request.user),
                    'username': request.user.username
                    }
                return render(request, 'rooms.html', context)
        context = {
                'form': ManageViewTimeSlotForm(),
                #'number': number,
                'time_slots': TimeSlot.objects.filter(manager=request.user),
                'username': request.user.username
                }
        return render(request, 'time_slots.html', context)
    else:
        return redirect('../book/')



"""Function that returns the list of bookings based on the search criteria."""
def manager_book_search(
        str_numbers, customer_name, str_check_in_date, str_check_in_time, str_check_out_time, category, person, no_of_rooms, manager):

    booking_list = Booking.objects.none()
    spaces_numbers = list(str_numbers.split(","))
    numbers = list()
    for i in spaces_numbers:
        numbers.append(i.strip())
    #check_in_date = convert_to_date(str_check_in_date)
    check_in_date = datetime.strptime(str_check_in_date, '%Y-%m-%d').date()

    #check_in_time = convert_to_time(str_check_in_time)
    check_in_time = datetime.strptime(str_check_in_time, '%H:%M').time()

    #check_out_time = convert_to_time(str_check_out_time)
    check_out_time = datetime.strptime(str_check_out_time, '%H:%M').time()

    for number in numbers:
        room_number_regex = rf"\b{number}\b"
        '''keys = ['room_numbers__iregex', 'customer_name', 'check_in_date', 'check_in_time__gte', 'check_out_time__lte', 'category__in', 'person__in', 'no_of_rooms', 'room_managers__regex']
        values = [room_number_regex, customer_name, check_in_date, check_in_time, check_out_time, category, person, no_of_rooms, room_manager_regex]'''
        keys = ['numbers__iregex', 'customer_name', 'check_in_date', 'check_in_time__gte', 'check_out_time__lte', 'category__in', 'person__in', 'no_of_rooms', 'room_managers__regex']
        values = [room_number_regex, customer_name, check_in_date, check_in_time, check_out_time, category, person, no_of_rooms]
        parameters = {}
        for key, value in zip(keys, values):
            if value is not None and value !=[] and value != '':
                parameters[key] = value
        booking_list = Booking.objects.filter(**parameters).union(booking_list).order_by('-check_in_date', 'check_in_time')
    return booking_list

"""Function to display bookings based on the selected criteria."""
@login_required(login_url="/hotel/sign_in/")
def manage_bookings(request):
    if request.user.email.endswith("@anshul.com"):
        bookings = Booking.objects.filter(manager=request.user)
        if request.method == 'POST':
            form = ManageBookingForm(request.POST)
            if form.is_valid():
                request.session['numbers'] = request.POST['numbers']
                #print(request.session['numbers'])
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
                response = manager_book_search(request.session['numbers'],
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

"""Function to book the time slot."""
def time_booking(
        numbers, room_type, no_of_rooms_required, username,
        book_date, check_in, check_out, person, room_managers):
    #for i in range(no_of_rooms_required):
        #room_no = numbers.pop()
    #print(numbers)


    # getting the comma-separated string from the list
    room_numbers_string = ", ".join([str(item) for item in numbers if item])
    room_managers_string = ", ".join([str(item) for item in room_managers if item])

    time_slot = Booking(customer_name=username,
                        check_in_date=book_date,
                        check_in_time=check_in,
                        check_out_time=check_out,
                        numbers=room_numbers_string,
                        category=room_type, person=person,
                        no_of_rooms = no_of_rooms_required,
                        room_managers=room_managers_string)
    time_slot.save()

def bubbleSort(time_slots):
    swapped = False
    # Looping from size of array from last index[-1] to index [0]
    for n in range(len(time_slots)-1, 0, -1):
        for i in range(n):
            if (datetime.combine(date.today(), time_slots[i].available_till) - datetime.combine(date.today(), time_slots[i].available_from)) > (datetime.combine(date.today(), time_slots[i + 1].available_till) - datetime.combine(date.today(), time_slots[i + 1].available_from)):
                swapped = True
                # swapping data if the element is less than next element in the array
                time_slots[i], time_slots[i + 1] = time_slots[i + 1], time_slots[i]       
        if not swapped:
            # exiting the function if we didn't make a single swap
            # meaning that the array is already sorted.
            return

"""Function to check if the room(s) is/are available."""
def available_time_slots(
        room_type, book_date_str,check_in_str,
        check_out_str, person, no_of_rooms_required):
    # Converting string to date.
    book_date = datetime.strptime(book_date_str, '%Y-%m-%d').date()
    check_in = datetime.strptime(check_in_str, '%H:%M').time()
    check_out = datetime.strptime(check_out_str, '%H:%M').time()




    # Converting string to date.
    # book_date = datetime.datetime.strptime(book_date_str, '%Y-%m-%d').date()
    # check_in = datetime.datetime.strptime(check_in_str, '%H:%M').time()
    # check_out = datetime.datetime.strptime(check_out_str, '%H:%M').time()

    room_list = Room.objects.filter(
        capacity__gte=person,
        category=room_type
    ).order_by('capacity')
    # regular_rooms = 0
    # executive_rooms = 0
    # deluxe_rooms = 0
    #time_slots = TimeSlot.objects.none()
    #count_time_slots = 0
    time_slots = list()
    #print(room_list)
    for room in room_list:
        # Calculating the maximum date to which a room can be
        # booked in advance.
        max_book = now + timedelta(days=room.advance)
        if (book_date <= max_book.date()):
            try:
                # time_slots = TimeSlot.objects.get(
                #     room=room,
                #     available_from_lte=check_in,
                #     available_till_gte=check_out,
                # ).union(time_slots)

                time_slot = TimeSlot.objects.get(
                    room=room,
                    available_from__lte=check_in,
                    available_till__gte=check_out,
                )
            except Exception:
                continue
            try:
                #taken = Booking.objects.get(Q(time_slot_ids__contains=time_slot.id)
                #                            & Q(check_in_date=book_date))
                Booking.objects.get(Q(time_slot_ids__contains=time_slot.id)
                                            & Q(check_in_date=book_date))
            except Exception:
            #if not taken:
                time_slots.append(time_slot)
                if len(time_slots) == no_of_rooms_required:
                    bubbleSort(time_slots)
                    return time_slots
    return time_slots

    #if len(time_slots) >= no_of_rooms_required:

        #bubbleSort(time_slots)

        # for i in range(len(time_slots)):
        #print(time_slots)
        #return time_slots

    #             if (time_slot.room.category == 'Regular'):
    #                 regular_rooms = regular_rooms + 1
    #             elif (time_slot.room.category == 'Executive'):
    #                 executive_rooms = executive_rooms + 1
    #             elif (time_slot.room.category == 'Deluxe'):
    #                 deluxe_rooms = deluxe_rooms + 1

    #             if (regular_rooms == no_of_rooms_required and time_slot.room.category == 'Regular'):
    #                 available_categories.append('Regular')
    #             if (executive_rooms == no_of_rooms_required and time_slot.room.category == 'Executive'):
    #                 available_categories.append('Executive')
    #             if (deluxe_rooms == no_of_rooms_required and time_slot.room.category == 'Deluxe'):
    #                 available_categories.append('Deluxe')
    #     return HttpResponse("Not Available")
    # return available_categories







    
    # regular_rooms = 0
    # executive_rooms = 0
    # deluxe_rooms = 0
    # # king_rooms = 0
    # # queen_rooms = 0
    # numbers = list()
    # room_managers = list()
    # # List of rooms for the given category.
    # try:
    #     room_list = Room.objects.filter(
    #         available_from__lte=check_in,
    #         available_till__gte=check_out,
    #         capacity__gte=person, category=room_type
    #     )
    # except Exception:
    #     return 3
    # for room in room_list:
    #     max_book = now + datetime.timedelta(days=room.advance)
    #     if (book_date <= max_book.date()):
    #         # To ensure no rooms are booked within a gap of 1 hour
    #         # after checkout.
    #         added_check_out = check_out.replace(
    #             hour=(check_out.hour + 1) % 24
    #         )
    #         # To ensure no rooms are booked within a gap of 1 hour
    #         # before check-in.
    #         subtracted_check_in = check_in.replace(
    #             hour=(check_in.hour - 1) % 24
    #         )
    #         taken = Booking.objects.filter(
    #             Q(Q(check_in_time__lt=added_check_out)
    #               | Q(check_out_time__gt=subtracted_check_in))
    #             & Q(room_numbers__contains=room.number)
    #             & Q(check_in_date=book_date))
    #         if not taken:
    #             if (room_type == 'Regular'):
    #                 regular_rooms = regular_rooms + 1
    #                 numbers.append(room.number)
    #                 room_managers.append(room.manager)
    #             elif (room_type == 'Executive'):
    #                 executive_rooms = executive_rooms + 1
    #                 numbers.append(room.number)
    #                 room_managers.append(room.manager)
    #             elif (room_type == 'Deluxe'):
    #                 deluxe_rooms = deluxe_rooms + 1
    #                 numbers.append(room.number)
    #                 room_managers.append(room.manager)
    #             elif (room_type == 'King'):
    #                 king_rooms = king_rooms + 1
    #                 numbers.append(room.number)
    #                 room_managers.append(room.manager)
    #             elif (room_type == 'Queen'):
    #                 queen_rooms = queen_rooms + 1
    #                 numbers.append(room.number)
    #                 room_managers.append(room.manager)
    #             if (room_type == 'Regular' and
    #                 regular_rooms == no_of_rooms_required  and room.category == 'Regular'):
    #                 time_booking(numbers, room_type, no_of_rooms_required,
    #                                 username, book_date, check_in,
    #                                 check_out, person, room_managers)
    #                 return 1
    #             elif (room_type == 'Executive' and
    #                 executive_rooms == no_of_rooms_required and room.category == 'Executive'):
    #                 time_booking(numbers, room_type, no_of_rooms_required,
    #                                 username, book_date, check_in,
    #                                 check_out, person)
    #                 return 1
    #             elif (room_type == 'Deluxe' and
    #                 deluxe_rooms == no_of_rooms_required and room.category == 'Deluxe'):
    #                 time_booking(numbers, room_type, no_of_rooms_required,
    #                                 username, book_date, check_in,
    #                                 check_out, person)
    #                 return 1
    #             elif (room_type == 'King' and
    #                 king_rooms == no_of_rooms_required and room.category == 'King'):
    #                 time_booking(numbers, room_type, no_of_rooms_required,
    #                                 username, book_date, check_in,
    #                                 check_out, person)
    #                 return 1
    #             elif (room_type == 'Queen' and
    #                 queen_rooms == no_of_rooms_required and room.category == 'Queen'):
    #                 time_booking(numbers, room_type, no_of_rooms_required,
    #                                 username, book_date, check_in,
    #                                 check_out, person)
    #                 return 1
    # return 2





def slots_booking(response, request):
    time_slot_ids = list()
    for i in range(len(response)):
        time_slot_ids.append(response[i].id)

    # getting the comma-separated string from the list
    time_slot_ids_string = ", ".join([str(item) for item in time_slot_ids if item])

    booking = Booking(customer_name=request.user.username,
                    check_in_date=request.session['book_date'],
                    time_slot_ids=time_slot_ids_string)
    booking.save()

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/sign_in/")
def regular(request):
    if request.method == 'POST':
        response = available_time_slots('Regular',
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
        if response != []:
            slots_booking(response, request)
            return redirect('../booked_regular/')
        context = {
            'category': 'Regular',
            'book_date': request.session['book_date'],
            'check_in': request.session['check_in'],
            'check_out': request.session['check_out'],
            'person': request.session['person'],
            'no_of_rooms_required': request.session['no_of_rooms_required'],
            'time_slots': response,
            'username': request.user.username
            }
        return render(request, 'available_time_slots.html', context)
        # time_slot_ids = list()
        # for i in range(len(response)):
        #     time_slot_ids.append(response[i].id)

        # # getting the comma-separated string from the list
        # time_slot_ids_string = ", ".join([str(item) for item in time_slot_ids if item])

        # booking = Booking(customer_name=request.user.username,
        #                 check_in_date=request.session['book_date'],
        #                 time_slot_ids=time_slot_ids_string)
        # booking.save()
        # Implemented Post/Redirect/Get.
        
    response = available_time_slots('Regular',
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
    context = {
        'category': 'Regular',
        'book_date': request.session['book_date'],
        'check_in': request.session['check_in'],
        'check_out': request.session['check_out'],
        'person': request.session['person'],
        'no_of_rooms_required': request.session['no_of_rooms_required'],
        'time_slots': response,
        'username': request.user.username
        }
    return render(request, 'available_time_slots.html', context)

    if response == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_regular/')
    elif response == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/sign_in/")
def executive(request):
    response = available_time_slots('Executive',
                                request.user.username,
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
    if response == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_executive/')
    elif response == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/sign_in/")
def deluxe(request):
    response = available_time_slots('Deluxe', request.user.username,
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
    if response == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_deluxe/')
    elif response == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/sign_in/")
def king(request):
    response = available_time_slots('King', request.user.username,
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
    if response == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_king/')
    elif response == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/sign_in/")
def queen(request):
    response = available_time_slots('Queen', request.user.username,
                                request.session['book_date'],
                                request.session['check_in'],
                                request.session['check_out'],
                                request.session['person'],
                                request.session['no_of_rooms_required'])
    if response == 1:
        # Implemented Post/Redirect/Get.
        return redirect('../booked_queen/')
    elif response == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/sign_in/")
def booked_regular(request):
    time_slot_bookings = Booking.objects.filter(
        customer_name=request.user.username,
        check_in_date=request.session['book_date']
    )
    print(time_slot_bookings)
    try:
        context = {'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
                'category': 'Regular',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/sign_in/")
def booked_executive(request):
    try:
        context = {'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
                'category': 'Executive',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/sign_in/")
def booked_deluxe(request):
    try:
        context = {'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
                'category': 'Deluxe',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/sign_in/")
def booked_king(request):
    try:
        context = {'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
                'category': 'King',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to show the booking for regular category.
Used for implementing Post/Redirect/Get."""
@login_required(login_url="/hotel/sign_in/")
def booked_queen(request):
    try:
        context = {'book_date': request.session['book_date'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
                'person': request.session['person'],
                'no_of_rooms_required': request.session['no_of_rooms_required'],
                'category': 'Queen',
                'username': request.user.username}
    except Exception:
        return redirect('../book/')
    return render(request, 'booked.html', context)

"""Function to return all the bookings."""
@login_required(login_url="/hotel/sign_in/")
def all_bookings(request, pk=None):
    if pk:
        try:
            booking = Booking.objects.get(pk=pk)
        except Exception:
            return HttpResponse("Not Found.")
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
            print("Fvfrf")
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
    regular_rooms = 0
    executive_rooms = 0
    deluxe_rooms = 0
    king_rooms = 0
    queen_rooms = 0
    numbers = list()
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
        max_book = now + timedelta(days=room.advance)
        # Ensuring that books are book before a room max advance
        if (request.session['api_book_date'] <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = request.session['api_check_out'].replace(
                hour=(request.session['api_check_out'].hour + 1) % 24
            )
            # To ensure no rooms are booked within a gap of 1 hour
            # before check-in.
            subtracted_check_in = request.session['api_check_in'].replace(
                hour=(request.session['api_check_in'].hour - 1) % 24
            )
            taken = Booking.objects.filter(
                Q(Q(check_in_time__lt=added_check_out)
                  | Q(check_out_time__gt=subtracted_check_in))
                & Q(room_numbers__contains=room.number)
                & Q(check_in_date=request.session['api_book_date']))
            if not taken:
                if (category == 'Regular'):
                    regular_rooms = regular_rooms + 1
                    numbers.append(room.number)
                elif (category == 'Executive'):
                    executive_rooms = executive_rooms + 1
                    numbers.append(room.number)
                elif (category == 'Deluxe'):
                    deluxe_rooms = deluxe_rooms + 1
                    numbers.append(room.number)
                elif (category == 'King'):
                    king_rooms = king_rooms + 1
                    numbers.append(room.number)
                elif (category == 'Queen'):
                    queen_rooms = queen_rooms + 1
                    numbers.append(room.number)
                if (category == 'Regular' and
                    regular_rooms == request.session['no_of_rooms']):
                    time_booking(numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Executive' and
                    executive_rooms == request.session['no_of_rooms']):
                    time_booking(numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Deluxe' and
                    deluxe_rooms == request.session['no_of_rooms']):
                    time_booking(numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'King' and
                    king_rooms == request.session['no_of_rooms']):
                    time_booking(numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
                elif (category == 'Queen' and
                    queen_rooms == request.session['no_of_rooms']):
                    time_booking(numbers, category, request.session['no_of_rooms'],
                                    request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                                    request.session['api_check_out'], request.session['api_person'])
                    return Response({'msg': 'Booked'})
    return Response({'msg': 'Unavailable.'})

    '''            time_slot = Booking(
                    customer_name=request.session['api_username'],
                    check_in_date=request.session['api_book_date'],
                    check_in_time=request.session['api_check_in'],
                    check_out_time=request.session['api_check_out'],
                    number=room.number,
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
