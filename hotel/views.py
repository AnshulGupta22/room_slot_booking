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
from hotel.forms import HotelForm, SigninForm, BookForm, AvailabilityForm
from django.http import HttpResponse
from . models import Booking, Room
import datetime

# Create your views here.
username = ''
# Function to convert string to datetime
def convert(date_time):
    #format = '%I:%M' # The format
    format = '%Y-%m-%d %H:%M'
    datetime_str = datetime.datetime.strptime(date_time, format).time()
   
    return datetime_str
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

def booking_algo(room_number, converted_start_time, converted_end_time, book_st, bookEn, slot):
    new_slot = TimeSlot.objects.get(room_number=room_number)
    flag = 0
    end_flag = 0
    success = False
    if(new_slot.room_available_from1 == None and new_slot.room_available_till1 == None):
        if flag == 0:
            new_slot.room_available_from1 = book_st
            new_slot.room_available_till1 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from1 = converted_end_time
            new_slot.room_available_till1 = bookEn
            end_flag = 1
    if(new_slot.room_available_from2 == None and new_slot.room_available_till2 == None):
        if flag == 0:   
            new_slot.room_available_from2 = book_st
            new_slot.room_available_till2 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from2 = converted_end_time
            new_slot.room_available_till2 = bookEn
            end_flag = 1
    if(new_slot.room_available_from3 == None and new_slot.room_available_till3 == None):
        if flag == 0:
            new_slot.room_available_from3 = book_st
            new_slot.room_available_till3 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from3 = converted_end_time
            new_slot.room_available_till3 = bookEn
            end_flag = 1
    if(new_slot.room_available_from4 == None and new_slot.room_available_till4 == None):
        if flag == 0:
            new_slot.room_available_from4 = book_st
            new_slot.room_available_till4 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from4 = converted_end_time
            new_slot.room_available_till4 = bookEn
            end_flag = 1
    if(new_slot.room_available_from5 == None and new_slot.room_available_till5 == None):
        if flag == 0:
            new_slot.room_available_from5 = book_st
            new_slot.room_available_till5 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from5 = converted_end_time
            new_slot.room_available_till5 = bookEn
            end_flag = 1
    if(new_slot.room_available_from6 == None and new_slot.room_available_till6 == None):
        if flag == 0:
            new_slot.room_available_from6 = book_st
            new_slot.room_available_till6 = converted_start_time
            flag = 1
        elif end_flag == 0:
            new_slot.room_available_from6 = converted_end_time
            new_slot.room_available_till6 = bookEn
            end_flag = 1
    if(flag == 1 and end_flag == 1):
        success = True
    #else:
    #    return HttpResponse("Not booked. Please contact room manager.")
    if slot == 1:
        new_slot.room_available_from1 = None
        new_slot.room_available_till1 = None
    elif slot == 2:
        new_slot.room_available_from2 = None
        new_slot.room_available_till2 = None
    elif slot == 3:
        new_slot.room_available_from3 = None
        new_slot.room_available_till3 = None
    elif slot == 4:
        new_slot.room_available_from4 = None
        new_slot.room_available_till4 = None
    elif slot == 5:
        new_slot.room_available_from5 = None
        new_slot.room_available_till5 = None
    elif slot == 6:
        new_slot.room_available_from6 = None
        new_slot.room_available_till6 = None
    new_slot.save()
    return(success)
    #return HttpResponse("Booked")

def book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            room_number = request.POST['room_number']
            book_from = request.POST['book_from']
            book_till = request.POST['book_till']
            converted_start_time = convert(book_from)
            converted_end_time = convert(book_till)
            #print(room_number)
            #sample_instance = TimeSlot.objects.get(id=1)
            #print(sample_instance.room_number)
            #rooms = TimeSlot.objects.all()
            #print(type([e.room_number for e in TimeSlot.objects.all()][0]))
            #print(type(int(room_number)))
            #sdf = int(room_number)
            #for i in range(1,7): 
            #print(TimeSlot.objects.room_number())
            #print([e.room_number for e in TimeSlot.objects.filter(room_number=room_number)])
            #if int(room_number) in [e.room_number for e in TimeSlot.objects.all()]:
            if int(room_number) in [e.room_number for e in TimeSlot.objects.filter(room_number=room_number)]:
                book_start = [e.room_available_from1 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                   if(book_start[0] <= converted_start_time):
                        book_end = [e.room_available_till1 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= converted_end_time):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 1)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
                                '''
                                new_slot = TimeSlot.objects.get(room_number=room_number)
                                flag = 0
                                if(new_slot.room_available_from2 == None and new_slot.room_available_till2 == None):
                                    new_slot.room_available_from2 = book_start[0]
                                    new_slot.room_available_till2 = converted_start_time
                                    global flag = 1
                                elif(new_slot.room_available_from3 == None and new_slot.room_available_till3 == None):
                                    if flag == 0:
                                        new_slot.room_available_from3 = book_start[0]
                                        new_slot.room_available_till3 = converted_start_time
                                        global flag = 1
                                    else:
                                        new_slot.room_available_from3 = converted_end_time
                                        new_slot.room_available_till3 = book_end[0]
                                elif(new_slot.room_available_from4 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from4 = book_start[0]
                                        new_slot.room_available_till4 = converted_start_time
                                        global flag = 1
                                    else:
                                        new_slot.room_available_from4 = converted_end_time
                                        new_slot.room_available_till4 = book_end[0]
                                elif(new_slot.room_available_from5 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from5 = book_start[0]
                                        new_slot.room_available_till5 = converted_start_time
                                    else:
                                        new_slot.room_available_from5 = converted_end_time
                                        new_slot.room_available_till5 = book_end[0]
                                elif(new_slot.room_available_from6 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from6 = book_start[0]
                                        new_slot.room_available_till6 = converted_start_time
                                    else:
                                        new_slot.room_available_from6 = converted_end_time
                                        new_slot.room_available_till6 = book_end[0]
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
                                new_slot.room_available_from1 = None
                                new_slot.room_available_till1 = None
                                new_slot.save()
                                return HttpResponse("Booked")'''
                
                book_start = [e.room_available_from2 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= converted_start_time):
                        book_end = [e.room_available_till2 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= converted_end_time):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 2)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
            
                book_start = [e.room_available_from3 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till3 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 3)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
            
                book_start = [e.room_available_from4 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till4 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 4)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
                book_start = [e.room_available_from5 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till5 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 5)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
                book_start = [e.room_available_from6 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till6 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 6)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
            return HttpResponse("Not available")
        else:
            context = {'form': BookForm()}
            return render(request, 'book.html', context)
    context = {'form': BookForm()}
    return render(request, 'book.html', context)
'''                
            book_start = [e.room_available_from1 for e in TimeSlot.objects.filter(room_number=room_number)]
            print(book_start)
            book_start = [e.room_available_from1 for e in TimeSlot.objects.all()]
            book_end = [e.room_available_till1 for e in TimeSlot.objects.all()]
            #print(convert(book_from))
            #print(book_start)
            #print(book_start[0] <= convert(book_from))
            #print(type(book_start[0]))
            return HttpResponse("Booked")
            #    else:
            #        return HttpResponse("Not available")'''
'''
                if book_till <= [e.room_available_till + str(i) for e in TimeSlot.objects.all()]:
            
            if int(room_number) in [e.room_number for e in TimeSlot.objects.all()]:
                return HttpResponse("Booked")
            else:
                return HttpResponse("Not available")'''
'''
            context = {'rooms': rooms}
            return redirect('signedin/')
            if user is not None:
                login(request, user)
                return redirect('signedin/')
            else:
                return HttpResponse("Invalid Credentials")
        else:
            context = {'form': form}
            return render(request, 'signin.html', context)'''
    
    
def welcome(request):
    return render(request,'welcome.html')
    
def signedin(request):
    return HttpResponse("Welcome user")
    '''
    rooms = TimeSlot.objects.all()
    context = {'rooms': rooms}
    return render(request, 'signedin.html', context)'''
    
def check_availability(category, check_in, check_out):
    avail_list = []
    
    #booking_list =  Room.objects.filter(category = category, book_from__lt = check_out, book_till__gt = check_in)
    room_list = Room.objects.filter(category = category)
    for room in room_list:
        #booking_list =  Room.objects.filter(category = category, book_from__lt = check_out,  book_till__gt = check_in)
        #booking_list =  Room.objects.filter(book_from__lt = check_out,  book_till__gt = check_in)
        #print(booking_list)
        #print(booking_list.values_list('room_number')[0][0])
        #booking_list =  Booking.objects.filter(category = category)
        #print(len(booking_list))
        booking_list = Room.objects.filter(book_from__lt = check_out,  book_till__gt = check_in)
        if not booking_list:
            booked_number = room.room_number
            time_slot = Room(user = username, book_from = check_in, book_till = check_out, room_number = booked_number, category = category)
            time_slot.save()
            return True
    #Room(category = category, book_from = check_out, book_till = check_in)
    return False
    '''
    print("lmbnb")
    for booking in booking_list:
        print("opin")
        if booking.book_from > check_out or booking.book_till < check_in:    
            avail_list.append(True)
        else:
            avail_listappend(False)
            print("rggrrg")
    return all(avail_list)
    '''
    
def booking(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            #user = request.POST['user']
            #room_number = request.POST['room_number']
            book_from = request.POST['book_from']
            book_till = request.POST['book_till']
            category = request.POST['category']
            #print(type(book_from))
            converted_start_time = convert(book_from)
            converted_end_time = convert(book_till)
            if(check_availability(category, book_from, book_till)):
                #Room username
                return HttpResponse("Booked")
                new_slot = Room.objects.get(category = category)
                new_slot.user = username
                new_slot.book_from = username
                new_slot.book_till = username
                new_slot.user = username
                #new_slot.room_available_till6 = bookEn
                new_slot.save()
                return HttpResponse("Booked")
            return HttpResponse("Not Booked")
            #print(room_number)
            #sample_instance = TimeSlot.objects.get(id=1)
            #print(sample_instance.room_number)
            #rooms = TimeSlot.objects.all()
            #print(type([e.room_number for e in TimeSlot.objects.all()][0]))
            #print(type(int(room_number)))
            #sdf = int(room_number)
            #for i in range(1,7): 
            #print(TimeSlot.objects.room_number())
            #print([e.room_number for e in TimeSlot.objects.filter(room_number=room_number)])
            #if int(room_number) in [e.room_number for e in TimeSlot.objects.all()]:
            if int(room_number) in [e.room_number for e in TimeSlot.objects.filter(room_number=room_number)]:
                book_start = [e.room_available_from1 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                   if(book_start[0] <= converted_start_time):
                        book_end = [e.room_available_till1 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= converted_end_time):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 1)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
                                '''
                                new_slot = TimeSlot.objects.get(room_number=room_number)
                                flag = 0
                                if(new_slot.room_available_from2 == None and new_slot.room_available_till2 == None):
                                    new_slot.room_available_from2 = book_start[0]
                                    new_slot.room_available_till2 = converted_start_time
                                    global flag = 1
                                elif(new_slot.room_available_from3 == None and new_slot.room_available_till3 == None):
                                    if flag == 0:
                                        new_slot.room_available_from3 = book_start[0]
                                        new_slot.room_available_till3 = converted_start_time
                                        global flag = 1
                                    else:
                                        new_slot.room_available_from3 = converted_end_time
                                        new_slot.room_available_till3 = book_end[0]
                                elif(new_slot.room_available_from4 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from4 = book_start[0]
                                        new_slot.room_available_till4 = converted_start_time
                                        global flag = 1
                                    else:
                                        new_slot.room_available_from4 = converted_end_time
                                        new_slot.room_available_till4 = book_end[0]
                                elif(new_slot.room_available_from5 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from5 = book_start[0]
                                        new_slot.room_available_till5 = converted_start_time
                                    else:
                                        new_slot.room_available_from5 = converted_end_time
                                        new_slot.room_available_till5 = book_end[0]
                                elif(new_slot.room_available_from6 == None and new_slot.room_available_till4 == None):
                                    if flag == 0:
                                        new_slot.room_available_from6 = book_start[0]
                                        new_slot.room_available_till6 = converted_start_time
                                    else:
                                        new_slot.room_available_from6 = converted_end_time
                                        new_slot.room_available_till6 = book_end[0]
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
                                new_slot.room_available_from1 = None
                                new_slot.room_available_till1 = None
                                new_slot.save()
                                return HttpResponse("Booked")'''
                
                book_start = [e.room_available_from2 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= converted_start_time):
                        book_end = [e.room_available_till2 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= converted_end_time):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 2)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
            
                book_start = [e.room_available_from3 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till3 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 3)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
            
                book_start = [e.room_available_from4 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till4 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 4)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
                book_start = [e.room_available_from5 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till5 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 5)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
                book_start = [e.room_available_from6 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] != None):
                    if(book_start[0] <= convert(book_from)):
                        book_end = [e.room_available_till6 for e in TimeSlot.objects.filter(room_number=room_number)]
                        if(book_end[0] != None):
                            if(book_end[0] >= convert(book_till)):
                                success = booking_algo(room_number, converted_start_time, converted_end_time, book_start[0], book_end[0], 6)
                                if(success == True):
                                    return HttpResponse("Booked")
                                else:
                                    return HttpResponse("Not booked. Please contact room manager.")
           
            return HttpResponse("Not available")
        else:
            context = {'form': BookForm()}
            return render(request, 'book.html', context)
    context = {'form': AvailabilityForm()}
    return render(request, 'book.html', context)
