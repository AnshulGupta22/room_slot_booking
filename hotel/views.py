from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (RoomSerializer, BookingSerializerBook,
                            BookingSerializerAdmin, BookingSerializerGet,
                            BookingSerializerAdminWithoutid,
                            CustomerAPISerializer)


from django.contrib.auth.models import User
from hotel.forms import CustomerForm, SignInForm, BookingForm
from .models import Room, Booking

# Create your views here.

now = timezone.now()

normal_username = None
normal_book_date = None
normal_check_in = None
normal_check_out = None
normal_capacity = None
ac_rooms = None
nac_rooms = None
deluxe_rooms = None
king_rooms = None
queen_rooms = None

api_username = None
api_book_date = None
api_check_in = None
api_check_out = None
api_capacity = None
api_ac_rooms = None
api_nac_rooms = None
api_deluxe_rooms = None
api_king_rooms = None
api_queen_rooms = None

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
            global normal_username
            normal_username = request.POST['desired_username']
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
            global normal_username
            normal_username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=normal_username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('../book/')

            else:
                return HttpResponse("Invalid credentials")

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
def check_availability(normal):
    if normal:
        book_date = normal_book_date
        check_in = normal_check_in
        check_out = normal_check_out
        capacity = normal_capacity

    else:
        book_date = api_book_date
        check_in = api_check_in
        check_out = api_check_out
        capacity = api_capacity

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
            taken = Booking.objects.filter(Q(Q(book_from_time__lt=added_check_out)
                                             | Q(book_till_time__gt=subtracted_check_in))
                                           & Q(room_number=room.room_number)
                                           & Q(book_from_date=book_date))
            if not taken:
                if room.category not in available_categories:

                    
                    # if (room.category == AC){
                    #   ac_rooms = ac_rooms + 1
                    # }
                    # if (room.category == NAC){
                    #   nac_rooms = nac_rooms + 1
                    # }
                    # if (room.category == KING){
                    #   king_rooms = king_rooms + 1
                    # }
                    # if (room.category == DELUXE){
                    #   deluxe_rooms = deluxe_rooms + 1
                    # }
                    # if (room.category == QUEEN){
                    #   queen_rooms = queen_rooms + 1
                    # }

                    # asd = 0
                    # if (room.category == KING){
                    # asd = asd++
                    # }
                    # if yui< no_of_rooms
                    # if no_of_rooms <= (select count * from room_list where category = AC)
                    ''' room_list = Room.objects.filter(
                            category=AC
                        ) '''
                    # select count * from room_list where category = NAC
                    # select count * from room_list where category = KING
                    # select count * from room_list where category = QUEEN
                    # select count * from room_list where category = DELUXE

                    # Appending available category.
                    available_categories.append(room.category)
    return available_categories

"""Function to return the available categories."""
@login_required(login_url="/hotel/signin/")
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            book_from_date = request.POST['book_from_date']
            book_from_time = request.POST['book_from_time']
            book_till_time = request.POST['book_till_time']
            global normal_book_date
            normal_book_date = convert_to_date(book_from_date)
            global normal_check_in
            normal_check_in = convert_to_time(book_from_time)
            # now is the date and time on which the user is booking.
            if (normal_book_date > now.date() or
                (normal_book_date == now.date() and
                normal_check_in >= now.time())):
                global normal_capacity
                normal_capacity = request.POST['capacity']
                global normal_check_out
                normal_check_out = convert_to_time(book_till_time)
                to_let = list()
                to_let = check_availability(True)
                if to_let:
                    response = to_let
                    context = {'categories': response}
                    return render(request, 'categories.html', context)
                return HttpResponse("Not Available")

            else:
                context = {'form': BookingForm()}
                return render(request, 'book.html', context)

        else:
            context = {'form': BookingForm()}
            return render(request, 'book.html', context)

    context = {'form': BookingForm()}
    return render(request, 'book.html', context)

def room_category(request, room_type):
    flag = False
    global normal_book_date
    global normal_check_in
    global normal_check_out
    global normal_capacity
    # List of rooms for the given category.
    room_list = Room.objects.filter(
        available_from__lte=normal_check_in,
        available_till__gte=normal_check_out,
        capacity__gte=normal_capacity, category=room_type
    )
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
                Q(Q(book_from_time__lt=added_check_out)
                  | Q(book_till_time__gt=subtracted_check_in))
                & Q(room_number=room.room_number)
                & Q(book_from_date=normal_book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=normal_username,
                    book_from_date=normal_book_date,
                    book_from_time=normal_check_in,
                    book_till_time=normal_check_out,
                    room_number=room.room_number,
                    category=room_type, capacity=normal_capacity
                )
                time_slot.save()

                normal_book_date = None
                normal_check_in = None
                normal_check_out = None
                category = None
                normal_capacity = None
                flag = True
                return flag
    normal_book_date = None
    normal_check_in = None
    normal_check_out = None
    category = None
    normal_capacity = None
    return flag

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def yac(request):
    flag = room_category(request, 'YAC')
    if flag:
        return render(request, 'booked.html')
    return HttpResponse("Unavailable")

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def nac(request):
    flag = room_category(request, 'NAC')
    if flag:
        return render(request, 'booked.html')
    return HttpResponse("Unavailable")

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def deluxe(request):
    flag = room_category(request, 'DEL')
    if flag:
        return render(request, 'booked.html')
    return HttpResponse("Unavailable")

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def king(request):
    flag = room_category(request, 'KIN')
    if flag:
        return render(request, 'booked.html')
    return HttpResponse("Unavailable")

"""Function to book room of this category if available."""
@login_required(login_url="/hotel/signin/")
def queen(request):
    flag = room_category(request, 'QUE')
    if flag:
        return render(request, 'booked.html')
    return HttpResponse("Unavailable")

"""Function to return all the bookings."""
@login_required(login_url="/hotel/signin/")
def all_bookings(request, pk=None):
    if pk:
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
        except:
            return HttpResponse("This booking no longer exists.")

    # Future bookings.
    future_bookings = Booking.objects.filter(
        customer_name=normal_username,
        book_from_date__gt=now.date()
    )
    # Current and past bookings.
    current_and_past_bookings = Booking.objects.filter(
        customer_name=normal_username, book_from_date__lte=now.date()
    )
    context = {
        'future_bookings': future_bookings,
        'current_and_past_bookings': current_and_past_bookings
    }
    return render(request, 'all_bookings.html', context)

"""API endpoints for User management, Rooms, Time Slots, and corresponding 
Bookings.
"""

@api_view(['GET', 'POST'])
def room_list(request, format=None):
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
def room_detail(request, pk, format=None):
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
def user_list(request, format=None):
    """
    To register a user.
    """
    if request.method == 'POST':
        serializer = CustomerAPISerializer(data=request.data)
        if serializer.is_valid():
            if(serializer.validated_data['password'] ==
                serializer.validated_data['confirm_password']):
                try:
                    user = User.objects.create_user(
                        serializer.validated_data['desired_username'],
                        serializer.validated_data['email'],
                        serializer.validated_data['password']
                    )
                    user.first_name = serializer.validated_data['first_name']
                    user.last_name = serializer.validated_data['last_name']
                    user.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                except:
                    return Response({'msg': 'Username already exist.'},
                                    status=
                                    status.HTTP_422_UNPROCESSABLE_ENTITY)

            else:
                return Response({'msg':
                    'Password and confirmation password do not match.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request, format=None):
    """
    List all bookings, or create a new booking.
    """
    global api_username
    api_username = request.user.username
    if request.method == 'GET':
        if request.user.is_active and request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-book_from_date')
            serializer = BookingSerializerAdmin(bookings, many=True)
            return Response(serializer.data)
        bookings = Booking.objects.filter(
                                            customer_name=api_username
                                         ).order_by('-book_from_date')
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
            global api_book_date
            api_book_date = serializer.validated_data['book_from_date']
            global api_check_in
            api_check_in = serializer.validated_data['book_from_time']
            # now is the date and time on which the user is booking.
            # Ensuring that booking is not done for past.
            if (api_book_date > now.date() or (api_book_date == now.date()
                and api_check_in >= now.time())):
                global api_check_out
                api_check_out = serializer.validated_data['book_till_time']
                global api_capacity
                api_capacity = serializer.validated_data['capacity']
                to_let = list()
                to_let = check_availability(False)
                if to_let:
                    response = to_let
                    context = {'categories': response}

                else:
                    context = dict()

                return Response(context)
            return Response({'msg': 'Cannot book for past.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_category(request, category, format=None):
    """
    To book a room for a given category.
    """
    global api_username
    global api_book_date
    global api_check_in
    global api_check_out
    global api_capacity

    # List of rooms for the given category.
    try:
        room_list = Room.objects.filter(
            available_from__lte=api_check_in,
            available_till__gte=api_check_out,
            capacity__gte=api_capacity, category=category
        )
    except:
        return Response({'msg': 'Unavailable'},
                        status=status.HTTP_404_NOT_FOUND)
    for room in room_list:
        max_book = now + datetime.timedelta(days=room.advance)
        # Ensuring that books are book before a room max advance
        if (api_book_date <= max_book.date()):
            # To ensure no rooms are booked within a gap of 1 hour
            # after checkout.
            added_check_out = api_check_out.replace(
                hour=(api_check_out.hour + 1) % 24
            )
            # To ensure no rooms are booked within a gap of 1 hour
            # before checkin.
            subtracted_check_in = api_check_in.replace(
                hour=(api_check_in.hour - 1) % 24
            )
            taken = Booking.objects.filter(
                Q(Q(book_from_time__lt=added_check_out)
                  | Q(book_till_time__gt=subtracted_check_in))
                & Q(room_number=room.room_number)
                & Q(book_from_date=api_book_date))
            if not taken:
                time_slot = Booking(
                    customer_name=api_username,
                    book_from_date=api_book_date,
                    book_from_time=api_check_in,
                    book_till_time=api_check_out,
                    room_number=room.room_number,
                    category=category, capacity=api_capacity
                )
                time_slot.save()

                api_username = None
                api_book_date = None
                api_check_in = None
                api_check_out = None
                category = None
                api_capacity = None
                return Response({'msg': 'Booked'})
        return Response({'msg': 'Unavailable.'},
                        status=status.HTTP_404_NOT_FOUND)
    api_username = None
    api_book_date = None
    api_check_in = None
    api_check_out = None
    category = None
    api_capacity = None
    return Response({'msg': 'Unavailable'}, status=status.HTTP_404_NOT_FOUND)

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
        field_value2 = getattr(obj, 'book_from_date')
        # To check if the deleted booking is for future.
        if (field_value2 > now.date()):
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'msg': 'Past booking'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    else:
        return Response({'msg': 'Not allowed'},
                        status=status.HTTP_403_FORBIDDEN)
