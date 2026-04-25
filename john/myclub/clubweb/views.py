from django.shortcuts import render, redirect
import calendar, csv,io
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event,Venue,MyClubuser
from .forms import VenueForm, EventForm, MyClubuserForm
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from django.db.models import Q
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

now = datetime.now()
year = now.year
month = now.strftime('%B')  
month_number = list(calendar.month_name).index(month.capitalize())
month_number = int(month_number)

#pagination 
def paginate_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    paginator = Paginator(event_list, 2) # Show 2 events per page
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    return render(request, 'clubweb/paginate_events.html', {'events': events})
#------------------------------------------------------------------------------------------------------
# generate pdf file venues list
def venues_pdf_file(request):
    venues = Venue.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venues.pdf"'
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    for venue in venues:
        p.drawString(100, y, f"Name: {venue.name}")
        p.drawString(100, y - 20, f"Address: {venue.address}")
        p.drawString(100, y - 40, f"Zip Code: {venue.zip_code}")
        p.drawString(100, y - 60, f"Phone: {venue.phone}")
        p.drawString(100, y - 80, f"Web: {venue.web}")
        p.drawString(100, y - 100, f"Email Address: {venue.email_address}")
        y -= 120
        
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='venues.pdf')
#------------------------------------------------------------------------------------------------------
# generate CSV file venues list
#------------------------------------------------------------------------------------------------------
def venues_csv_file(request):
    venues = Venue.objects.all()# get all venues from the database
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)# create a CSV writer object
    writer.writerow(['Name', 'Address', 'Zip Code', 'Phone', 'Web', 'Email Address'])# write the header row 
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response
#------------------------------------------------------------------------------------------------------
# generate text file venues list
#------------------------------------------------------------------------------------------------------
def venues_text_file(request):
    venues = Venue.objects.all()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venues.txt"'
    for venue in venues:
        response.write(f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n")
    return response 

#------------------------------------------------------------------------------------------------------
# Create your views here.
#------------------------------------------------------------------------------------------------------
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('clubweb:event_list')
#------------------------------------------------------------------------------------------------------
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid ():
        form.save()
        return redirect('clubweb:event_list')
    return render(request, 'clubweb/update_event.html',
                   {'event': event, 'form': form})
#------------------------------------------------------------------------------------------------------
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('clubweb:venues')
#------------------------------------------------------------------------------------------------------
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid ():
        form.save()
        return redirect('clubweb:venues')
    return render(request, 'clubweb/update_venue.html',
                   {'venue': venue, 'form': form})
#------------------------------------------------------------------------------------------------------

def add_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event/?submitted=True')
    else:
        form = EventForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'clubweb/add_event.html', {'form': form, 'submitted': submitted})

#------------------------------------------------------------------------------------------------------
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'clubweb/show_venue.html', {'venue': venue}) 
#------------------------------------------------------------------------------------------------------

def venues(request):
    venues = Venue.objects.all()
    paginator = Paginator(venues, 2) # Show 2 venues per page
    page = request.GET.get('page')  
    try:
        venues = paginator.page(page)
    except PageNotAnInteger:
        venues = paginator.page(1)
    except EmptyPage:
        venues = paginator.page(paginator.num_pages)
    return render(request, 'clubweb/venues.html', {'venues': venues})
#------------------------------------------------------------------------------------------------------

def search_venues(request):
    query = ''
    results = []
    if request.method == 'POST':
        query = request.POST.get('search', '').strip()
    else:
        query = request.GET.get('search', '').strip()

    if query:
        results = Venue.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(zip_code__icontains=query)
        )

    return render(request, 'clubweb/search_venue.html', {
        'query': query,
        'results': results,
    })
#------------------------------------------------------------------------------------------------------

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'clubweb/add_venue.html', {'form': form, 'submitted': submitted})
#------------------------------------------------------------------------------------------------------

def all_events(request):    
    #event_list = Event.objects.all().order_by('-event_date')
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 2) # Show 2 events per page
    page = request.GET.get('page')
    try:
        event_list = paginator.page(page)
    except PageNotAnInteger:
        event_list = paginator.page(1)
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)
    return render(request, 'clubweb/event_list.html', {
        'event_list': event_list,
    })
#------------------------------------------------------------------------------------------------------

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