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
from hotel.forms import HotelForm, SigninForm, BookForm
from django.http import HttpResponse
from . models import TimeSlot
import datetime

# Create your views here.

# Function to convert string to datetime
def convert(date_time):
    format = '%I:%M' # The format
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
def book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            room_number = request.POST['room_number']
            book_from = request.POST['book_from']
            book_till = request.POST['book_till']
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
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till1 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
                
                book_start = [e.room_available_from2 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till2 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
            
                book_start = [e.room_available_from3 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till3 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
            
                book_start = [e.room_available_from4 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till4 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
           
                book_start = [e.room_available_from5 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till5 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
           
                book_start = [e.room_available_from6 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till6 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")
           
                book_start = [e.room_available_from7 for e in TimeSlot.objects.filter(room_number=room_number)]
                if(book_start[0] <= convert(book_from)):
                    book_end = [e.room_available_till7 for e in TimeSlot.objects.filter(room_number=room_number)]
                    if(book_end[0] >= convert(book_till)):
                        return HttpResponse("Booked")

                return HttpResponse("Not available")
            else:
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
    rooms = TimeSlot.objects.all()
    context = {'rooms': rooms}
    return render(request, 'signedin.html', context)
    
