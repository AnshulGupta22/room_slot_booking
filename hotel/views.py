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

from hotel.forms import CustomerForm, SignInForm, BookingForm
from .models import Room, Booking

from .serializers import (
    RoomSerializer, BookingSerializerBook, BookingSerializerAdmin,
    BookingSerializerGet, BookingSerializerAdminWithoutid,
    CustomerAPISerializer
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
    datetime_str = datetime.datetime.strptime(date_time, format).date()
    return datetime_str

"""Function to convert string to time."""
def convert_to_time(date_time):
    format = '%H:%M'
    datetime_str = datetime.datetime.strptime(date_time, format).time()
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
                request.session['normal_username'] = request.POST['username']
                login(request, user)
                return redirect('../book/')
            except Exception:
                return HttpResponse("Something went wrong. Please try again.")
        else:
            context = {'form': form}
            return render(request, 'sign_up.html', context)
    context = {'form': CustomerForm()}
    return render(request, 'sign_up.html', context)

"""Function for viewing profile."""
@login_required(login_url="/hotel/signin/")
def view_profile(request):
    profile = User.objects.filter(
        username=request.session['normal_username']
        ).values()
    context = {'profile': profile}
    return render(request, 'view_profile.html', context)

"""Function for editing profile."""
@login_required(login_url="/hotel/signin/")
def edit_profile(request):
    profile = User.objects.get(username=request.session['normal_username'])
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'sign_up.html', context)
    context = {'form': CustomerForm(instance=profile)}
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
            request.session['normal_username'] = request.POST['username']
            login(request, user)
            return redirect('../book/')
        else:
            context = {'form': form}
            return render(request, 'sign_in.html', context)
    context = {'form': SignInForm()}
    return render(request, 'sign_in.html', context)

"""Function for log out."""
def logout_view(request):
    logout(request)
    return redirect('../signin/')

"""Function that returns the list of available categories."""
def search_availability(
        book_date, check_in, check_out,
        person, normal_no_of_rooms_required):
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
    return available_categories

"""Function to return the available categories."""
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            request.session['normal_book_date'] = request.POST['check_in_date']
            normal_book_date = convert_to_date(request.session['normal_book_date'])
            request.session['normal_check_in'] = request.POST['check_in_time']
            normal_check_in = convert_to_time(request.session['normal_check_in'])
            request.session['normal_check_out'] = request.POST['check_out_time']
            request.session['normal_person'] = int(request.POST['person'])
            request.session['normal_no_of_rooms_required'] = int(
                request.POST['no_of_rooms']
                )
            normal_check_out = convert_to_time(request.session['normal_check_out'])
            response = search_availability(normal_book_date,
                                           normal_check_in,
                                           normal_check_out,
                                           request.session['normal_person'],
                                           request.session['normal_no_of_rooms_required'])
            if response:
                context = {
                    'categories': response,
                    'username': request.session['normal_username']
                    }
                return render(request, 'categories.html', context)
            return HttpResponse("Not Available")
        else:
            context = {
                'form': form,
                'username': request.session['normal_username']
                }
            return render(request, 'book.html', context)
    context = {
        'form': BookingForm(),
        'username': request.session['normal_username']
        }
    return render(request, 'book.html', context)

"""Function to book the time slot."""
def time_booking(
        room_numbers, room_type, no_of_rooms_required, normal_username,
        normal_book_date, normal_check_in, normal_check_out, normal_person):
    #for i in range(no_of_rooms_required):
        #room_no = room_numbers.pop()
        #print(room_numbers)
    time_slot = Booking(customer_name=normal_username,
                        check_in_date=normal_book_date,
                        check_in_time=normal_check_in,
                        check_out_time=normal_check_out,
                        room_number=room_numbers,
                        category=room_type, person=normal_person,
                        no_of_rooms = no_of_rooms_required)
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
                & Q(room_number__contains=room.room_number)
                & Q(check_in_date=normal_book_date))
            if not taken:
                if (room_type == 'Regular'):
                    normal_regular_rooms = normal_regular_rooms + 1
                    room_numbers.append(room.room_number)
                elif (room_type == 'Executive'):
                    normal_executive_rooms = normal_executive_rooms + 1
                    room_numbers.append(room.room_number)
                elif (room_type == 'Deluxe'):
                    normal_deluxe_rooms = normal_deluxe_rooms + 1
                    room_numbers.append(room.room_number)
                elif (room_type == 'King'):
                    normal_king_rooms = normal_king_rooms + 1
                    room_numbers.append(room.room_number)
                elif (room_type == 'Queen'):
                    normal_queen_rooms = normal_queen_rooms + 1
                    room_numbers.append(room.room_number)
    if (room_type == 'Regular' and
        normal_regular_rooms >= normal_no_of_rooms_required):
        time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                        normal_username, normal_book_date, normal_check_in,
                        normal_check_out, normal_person)
        return 1
    elif (room_type == 'Executive' and
          normal_executive_rooms >= normal_no_of_rooms_required):
        time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                        normal_username, normal_book_date, normal_check_in,
                        normal_check_out, normal_person)
        return 1
    elif (room_type == 'Deluxe' and
          normal_deluxe_rooms >= normal_no_of_rooms_required):
        time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                        normal_username, normal_book_date, normal_check_in,
                        normal_check_out, normal_person)
        return 1
    elif (room_type == 'King' and
          normal_king_rooms >= normal_no_of_rooms_required):
        time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                        normal_username, normal_book_date, normal_check_in,
                        normal_check_out, normal_person)
        return 1
    elif (room_type == 'Queen' and
          normal_queen_rooms >= normal_no_of_rooms_required):
        time_booking(room_numbers, room_type, normal_no_of_rooms_required,
                        normal_username, normal_book_date, normal_check_in,
                        normal_check_out, normal_person)
        return 1
    return 2

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def regular(request):
    room_status = room_category('Regular', request.session['normal_username'],
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        context = {'username': request.session['normal_username']}
        return render(request, 'booked.html', context)
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def executive(request):
    room_status = room_category('Executive',
                                request.session['normal_username'],
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        context = {'username': request.session['normal_username']}
        return render(request, 'booked.html', context)
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def deluxe(request):
    room_status = room_category('Deluxe', request.session['normal_username'],
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        context = {'username': request.session['normal_username']}
        return render(request, 'booked.html', context)
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def king(request):
    room_status = room_category('King', request.session['normal_username'],
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        context = {'username': request.session['normal_username']}
        return render(request, 'booked.html', context)
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def queen(request):
    room_status = room_category('Queen', request.session['normal_username'],
                                request.session['normal_book_date'],
                                request.session['normal_check_in'],
                                request.session['normal_check_out'],
                                request.session['normal_person'],
                                request.session['normal_no_of_rooms_required'])
    if room_status == 1:
        context = {'username': request.session['normal_username']}
        return render(request, 'booked.html', context)
    elif room_status == 2:
        return HttpResponse("Unavailable")
    else:
        return redirect('../book/')

"""Function to return all the bookings."""
@login_required(login_url="/hotel/signin/")
def all_bookings(request, pk=None):
    if pk:
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
        except Exception:
            return HttpResponse("This booking no longer exists.")
    # Future bookings.
    future_bookings = Booking.objects.filter(
        customer_name=request.session['normal_username'],
        check_in_date__gt=now.date()
    )
    # Current and past bookings.
    current_and_past_bookings = Booking.objects.filter(
        customer_name=request.session['normal_username'],
        check_in_date__lte=now.date()
    )
    context = {
        'future_bookings': future_bookings,
        'current_and_past_bookings': current_and_past_bookings,
        'username': request.session['normal_username']
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    """
    List all bookings, or create a new booking.
    """
    request.session['api_username'] = request.user.username
    if request.method == 'GET':
        if request.user.is_active and request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-check_in_date')
            serializer = BookingSerializerAdmin(bookings, many=True)
            return Response(serializer.data)
        bookings = Booking.objects.filter(
                                            customer_name=request.session['api_username']
                                         ).order_by('-check_in_date')
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
            request.session['api_book_date'] = serializer.validated_data['check_in_date']
            request.session['api_check_in'] = serializer.validated_data['check_in_time']
            request.session['api_check_out'] = serializer.validated_data['check_out_time']
            request.session['api_person'] = serializer.validated_data['person']
            request.session['no_of_rooms'] = serializer.validated_data['no_of_rooms']
            response = search_availability(request.session['api_book_date'], request.session['api_check_in'], request.session['api_check_out'], request.session['api_person'], request.session['no_of_rooms'])
            print(type(request.session['api_book_date']))
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
                & Q(room_number__contains=room.room_number)
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
        normal_regular_rooms >= request.session['no_of_rooms']):
        time_booking(room_numbers, category, request.session['no_of_rooms'],
                        request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                        request.session['api_check_out'], request.session['api_person'])
        return Response({'msg': 'Booked'})
    elif (category == 'Executive' and
          normal_executive_rooms >= request.session['no_of_rooms']):
        time_booking(room_numbers, category, request.session['no_of_rooms'],
                        request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                        request.session['api_check_out'], request.session['api_person'])
        return Response({'msg': 'Booked'})
    elif (category == 'Deluxe' and
          normal_deluxe_rooms >= request.session['no_of_rooms']):
        time_booking(room_numbers, category, request.session['no_of_rooms'],
                        request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                        request.session['api_check_out'], request.session['api_person'])
        return Response({'msg': 'Booked'})
    elif (category == 'King' and
          normal_king_rooms >= request.session['no_of_rooms']):
        time_booking(room_numbers, category, request.session['no_of_rooms'],
                        request.session['api_username'], request.session['api_book_date'], request.session['api_check_in'],
                        request.session['api_check_out'], request.session['api_person'])
        return Response({'msg': 'Booked'})
    elif (category == 'Queen' and
          normal_queen_rooms >= request.session['no_of_rooms']):
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
