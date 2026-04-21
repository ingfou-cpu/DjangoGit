from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event,Venue,MyClubuser


now = datetime.now()
year = now.year
month = now.strftime('%B')  
month_number = list(calendar.month_name).index(month.capitalize())
month_number = int(month_number)
# Create your views here.


def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'clubweb/event_list.html', {
        'event_list': event_list,
    })

def home(request, years=now.year, month=now.month):
    #create a calendar
    cal = HTMLCalendar().formatmonth(years, month_number)
    #get current year
    now = datetime.now()
    current_year = now.year
    #get current time
    time = now.strftime('%I:%M  %p')      

    name = 'ingfou'
    return render(request, 'clubweb/home.html', {
        'fname': name,
        'years': years,
        'month': month,
        'month_number': month_number,
        'current_year': current_year,
        'time': time,
        'now': now,
        'cal': cal

        })    