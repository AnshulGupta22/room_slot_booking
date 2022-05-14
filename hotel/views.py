from django.shortcuts import render
from django.http import HttpResponse
from .models import Hotel

# Create your views here.

def index(request):
    return HttpResponse("Hello World")
    
def count_rooms(request):
    #count_rooms = Hotel.objects.count()
    #return HttpResponse(count_rooms)
    count_rooms = Hotel.objects.all()
    context = {'hot': count_rooms}
    return render(request, 'qwert.html', context)
