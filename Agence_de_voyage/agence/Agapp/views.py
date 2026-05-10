from django.shortcuts import render
from .models import Destination, Booking, Contact, Testimonial, pack_travel, Hotel

# Create your views here.

def home(request):
    bookings = Booking.objects.all()
    pack_travels = pack_travel.objects.all()
    Destinations = Destination.objects.all()
    return render(request, 'home.html', {'pack_travel' : pack_travels, 'Destination' : Destinations})   

def reservation(request):
    Hotels = Hotel.objects.all()
    Destinations = Destination.objects.all()
    customer_name = request.POST.get('customer_name', '')
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone_number = request.POST.get('phone_number')
        destination_id = request.POST.get('destination')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        hotel_id = request.POST.get('hotel')
        means_of_transport = request.POST.get('means_of_transport')
        
        try:
            destination = Destination.objects.get(id=destination_id) if destination_id else None
            hotel = Hotel.objects.get(id=hotel_id) if hotel_id else None
            
            if destination:
                booking = Booking(
                    customer_name=name,
                    customer_email=email,
                    phone_number=phone_number,
                    destination=destination,
                    hotel=hotel,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    means_of_transport=means_of_transport
                )
                booking.save()
        except (Destination.DoesNotExist, Hotel.DoesNotExist):
            pass
    return render(request, 'reservation.html', {'Hotels': Hotels, 'Destinations': Destinations, 'customer_name': customer_name})

def reselieuChoisi(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    hotels = Hotel.objects.filter(destination=destination)
    return render(request, 'reselieuChoisi.html', {'destination': destination, 'hotels': hotels})
