from django.shortcuts import render
from .models import Destination, Booking, Contact, Testimonial, pack_travel, Hotel
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def home(request):
    #bookings = Booking.objects.all()
    pack_travels = pack_travel.objects.all()
    Destinations = Destination.objects.all()
    return render(request, 'home.html', {'pack_travel' : pack_travels, 'Destination' : Destinations})   

def reservation(request):
    Hotels = Hotel.objects.all()
    Destinations = Destination.objects.all()
    customer_name = ''
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone_number = request.POST.get('phone_number')
        destination_id = request.POST.get('destination')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        hotel_id = request.POST.get('hotel')
        means_of_transport = request.POST.get('means_of_transport')
        customer_name = name or ''
        
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
    confirmation_message = None

    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone_number = request.POST.get('phone_number')
        hotel_id = request.POST.get('hotel')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        means_of_transport = request.POST.get('means_of_transport')

        try:
            hotel = Hotel.objects.get(id=hotel_id) if hotel_id else None
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
            confirmation_message = "✅ Votre réservation a été confirmée avec succès !"
        except Hotel.DoesNotExist:
            confirmation_message = "❌ Erreur : l'hôtel sélectionné n'existe pas."

    return render(request, 'reselieuChoisi.html', {
        'destination': destination,
        'hotels': hotels,
        'confirmation_message': confirmation_message
    })

def reservCroisiere(request, pack_travel_id):
    reserCoisiere.objects.filter(pack_travel_id=pack_travel_id).delete()
    pack_travel_instance = pack_travel.objects.get(id=pack_travel_id)
    customer_name = ''
    customer_email = ''
    customer_phone = ''
    nombre_personnes = 1
    nombre_enfants = 0
    confirmation_message = None
    show_confirmation = False

    if request.method == 'POST':
        step = request.POST.get('step', 'calcul')

        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone_number = request.POST.get('phone_number')
        nombre_personnes = request.POST.get('nombre_personnes')
        nombre_enfants = request.POST.get('nombre_enfants')
        customer_name = name or ''
        customer_email = email or ''
        customer_phone = phone_number or ''
        nb_personnes = int(nombre_personnes) if nombre_personnes else 1
        nb_enfants = int(nombre_enfants) if nombre_enfants else 0

        if step == 'calcul':
            # Étape 1 : afficher le récapitulatif de confirmation
            show_confirmation = True
        elif step == 'confirm':
            # Étape 2 : sauvegarder la réservation
            try:
                croisiere = reserCoisiere(
                    pack_travel=pack_travel_instance,
                    customer_name=name,
                    customer_email=email,
                    phone_number=phone_number,
                    nombre_personnes=nb_personnes,
                    nombre_enfants=nb_enfants
                )
                croisiere.save()
                confirmation_message = "✅ Votre réservation de croisière a été confirmée avec succès !"
            except Exception as e:
                confirmation_message = f"❌ Erreur lors de la réservation : {str(e)}"

    return render(request, 'reservCroisiere.html', {
        'pack_travel': pack_travel_instance,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'nombre_personnes': nombre_personnes,
        'nombre_enfants': nombre_enfants,
        'confirmation_message': confirmation_message,
        'show_confirmation': show_confirmation
    })

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('contact') + '?submitted=True')
            #return HttpResponseRedirect(reverse('contact?submitted=True'))
    else:
        form = ContactForm
        if 'submitted' in request.GET:
            submitted = True 
    return render(request, 'contact.html', {'form': form, 'submitted': submitted})

def about(request):
    return render(request, 'about.html', {})

def croisiere(request):
     pack_travels = pack_travel.objects.all()
     return render(request, 'croisiere.html', {'pack_travel': pack_travels})