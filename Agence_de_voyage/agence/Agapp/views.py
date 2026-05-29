from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination, Booking, Contact, Testimonial, pack_travel, Hotel, reser_circuit, PaymentRecord
from .forms import ContactForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
import stripe
from django.contrib.messages.views import SuccessMessageMixin
import logging
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

# Create your views here.-


"""def home(request):
    #bookings = Booking.objects.all()
    pack_travels = pack_travel.objects.all()
    Destinations = Destination.objects.all()
    return render(request, 'home.html', {'pack_travel': pack_travels, 'Destination': Destinations})
"""
class HomeView(ListView):
    model = Destination
    paginate_by = 2 # Nombre d'éléments par page
    template_name = 'home.html'
    context_object_name = 'Destination'#Avec ListView et model = Destination, Django crée automatiquement la variable object_list (et non Destination).
    extra_context = {'pack_travels': pack_travel.objects.all()}
    extra_context = {'hotels': Hotel.objects.all()}
    extra_context = {'bookings': Booking.objects.all()}
    extra_context = {'testimonials': Testimonial.objects.all()}
    
"""    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pack_travels'] = pack_travel.objects.all()
        context['hotels'] = Hotel.objects.all()
        context['bookings'] = Booking.objects.all()
        context['testimonials'] = Testimonial.objects.all()
        return context"""

class contactcreteview(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact') # redirige vers la même page après soumission du formulaire
    success_message = "✅ Votre message a été envoyé avec succès !"
    
"""def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact') + '?submitted=True')
    else:
        form = ContactForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'contact.html', {'form': form, 'submitted': submitted})"""

class temoignageViewV(CreateView):
    model = Testimonial
    template_name = 'testimonial_form.html' # On peut aussi utiliser 'temoignage.html' à la place de 'testimonial_form.html' pour afficher les témoignages dans une page dédiée
    fields = ['customer_name', 'destination', 'rating', 'comment']
    context_object_name = 'Testimonial'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Le livre a été créé avec succès.")
        return response
    success_url = reverse_lazy('temoignage') # redirige vers la page de témoignages après soumission du formulaire

"""def temoignage(request):
    testimonials = Testimonial.objects.all()
    destinations = Destination.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'temoignage.html',{'Testimonial': testimonials, 'Destination': destinations,'Booking': bookings})
"""
class temoignageView(ListView):
    model = Testimonial
    paginate_by = 2 # Nombre d'éléments par page
    template_name = 'temoignage.html'
    context_object_name = 'Testimonial'#Avec ListView et model = Testimonial, Django crée automatiquement la variable object_list (et non Testimonial).

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
    pack_travel_instance = get_object_or_404(pack_travel, id=pack_travel_id)
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
            show_confirmation = True
        elif step == 'confirm':
            try:
                reservation = reser_circuit(
                    pack_travel=pack_travel_instance,
                    customer_name=name,
                    customer_email=email,
                    phone_number=phone_number,
                )
                reservation.save()
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

def about(request):
    return render(request, 'about.html', {})


def croisiere(request):
    pack_travels = pack_travel.objects.all()
    return render(request, 'croisiere.html', {'pack_travel': pack_travels})


#-----------------------------circuit------------------------------------------------------------
def circuit(request):
    pack_travels = pack_travel.objects.all()
    Destinations = Destination.objects.all()
    return render(request, 'circuit_touris.html', {'Destination': Destinations, 'pack_travels': pack_travels})


def circuitChoisi(request, pack_travel_id):
    pack_travels = pack_travel.objects.get(id=pack_travel_id)
    confirmation_message = None

    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone_number = request.POST.get('phone_number')

        try:
            booking = reser_circuit(
                customer_name=name,
                customer_email=email,
                phone_number=phone_number,
                pack_travel=pack_travels
            )
            booking.save()
            confirmation_message = "✅ Votre réservation a été confirmée avec succès !"
        except Exception as e:
            confirmation_message = f"❌ Erreur : {str(e)}"

    return render(request, 'circuitChoisi.html', {
        'pack_travels': pack_travels,
        'confirmation_message': confirmation_message
    })


#============================= VUES PAIEMENT STRIPE =============================#

def payment_home(request):
    """Page de paiement avec liste des destinations et packs"""
    destinations = Destination.objects.all()
    packs = pack_travel.objects.all()
    context = {
        'destinations': destinations,
        'packs': packs,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payment_home.html', context)


def create_checkout_destination(request, destination_id):
    """Crée une session de paiement Stripe pour une destination"""
    if request.method != "POST":
        return redirect('payment_home')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    destination = get_object_or_404(Destination, id=destination_id)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"Voyage - {destination.name}",
                            "description": destination.description or f"Réservation pour {destination.name}",
                        },
                        "unit_amount": int(destination.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
            metadata={
                'type': 'destination',
                'destination_id': destination.id,
                'customer_name': request.POST.get('customer_name', ''),
                'customer_email': request.POST.get('customer_email', ''),
                'customer_phone': request.POST.get('customer_phone', ''),
            }
        )

        PaymentRecord.objects.create(
            destination=destination,
            stripe_checkout_session_id=checkout_session.id,
            amount=destination.price,
            customer_name=request.POST.get('customer_name', ''),
            customer_email=request.POST.get('customer_email', ''),
            customer_phone=request.POST.get('customer_phone', ''),
            status='pending',
        )

        return redirect(checkout_session.url, code=303)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        messages.error(request, f"Erreur de paiement: {str(e)}")
        return redirect('payment_home')
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        messages.error(request, "Une erreur inattendue s'est produite.")
        return redirect('payment_home')


def create_checkout_pack(request, pack_id):
    """Crée une session de paiement Stripe pour un pack/circuit"""
    if request.method != "POST":
        return redirect('payment_home')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    pack = get_object_or_404(pack_travel, id=pack_id)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"Pack - {pack.pack_name}",
                            "description": pack.description or f"Pack voyage: {pack.pack_name}",
                        },
                        "unit_amount": int(pack.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
            metadata={
                'type': 'pack',
                'pack_id': pack.id,
                'customer_name': request.POST.get('customer_name', ''),
                'customer_email': request.POST.get('customer_email', ''),
                'customer_phone': request.POST.get('customer_phone', ''),
            }
        )

        PaymentRecord.objects.create(
            pack=pack,
            stripe_checkout_session_id=checkout_session.id,
            amount=pack.price,
            customer_name=request.POST.get('customer_name', ''),
            customer_email=request.POST.get('customer_email', ''),
            customer_phone=request.POST.get('customer_phone', ''),
            status='pending',
        )

        return redirect(checkout_session.url, code=303)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        messages.error(request, f"Erreur de paiement: {str(e)}")
        return redirect('payment_home')
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        messages.error(request, "Une erreur inattendue s'est produite.")
        return redirect('payment_home')


def payment_success(request):
    """Page de succès après un paiement Stripe"""
    session_id = request.GET.get('session_id')
    payment_record = None

    if session_id:
        try:
            payment_record = PaymentRecord.objects.get(
                stripe_checkout_session_id=session_id
            )
            payment_record.status = 'completed'
            payment_record.save()

            # Créer la réservation automatiquement
            if payment_record.destination and payment_record.customer_name:
                Booking.objects.create(
                    destination=payment_record.destination,
                    customer_name=payment_record.customer_name,
                    customer_email=payment_record.customer_email,
                    phone_number=payment_record.customer_phone,
                )
            elif payment_record.pack and payment_record.customer_name:
                reser_circuit.objects.create(
                    pack_travel=payment_record.pack,
                    customer_name=payment_record.customer_name,
                    customer_email=payment_record.customer_email,
                    phone_number=payment_record.customer_phone,
                )

        except PaymentRecord.DoesNotExist:
            logger.warning(f"Payment record not found: {session_id}")

    return render(request, 'payment_success.html', {'payment_record': payment_record})


def payment_cancel(request):
    """Page d'annulation de paiement"""
    return render(request, 'payment_cancel.html')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Webhook pour gérer les événements Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)

    event_type = event['type']
    logger.info(f"Received Stripe event: {event_type}")

    if event_type == 'checkout.session.completed':
        handle_checkout_completed(event['data']['object'])
    elif event_type == 'checkout.session.expired':
        handle_checkout_expired(event['data']['object'])
    elif event_type == 'payment_intent.succeeded':
        handle_payment_succeeded(event['data']['object'])
    elif event_type == 'payment_intent.payment_failed':
        handle_payment_failed(event['data']['object'])

    return HttpResponse(status=200)


def handle_checkout_completed(session):
    """Gère l'événement checkout.session.completed"""
    session_id = session.get('id')
    try:
        payment = PaymentRecord.objects.get(stripe_checkout_session_id=session_id)
        payment.status = 'completed'
        payment.stripe_customer_id = session.get('customer', '')
        payment.stripe_payment_intent_id = session.get('payment_intent', '')
        payment.save()
        logger.info(f"Payment completed: {session_id}")
    except PaymentRecord.DoesNotExist:
        logger.warning(f"Payment not found: {session_id}")


def handle_checkout_expired(session):
    """Gère l'événement checkout.session.expired"""
    session_id = session.get('id')
    try:
        payment = PaymentRecord.objects.get(stripe_checkout_session_id=session_id)
        payment.status = 'expired'
        payment.save()
    except PaymentRecord.DoesNotExist:
        pass


def handle_payment_succeeded(payment_intent):
    """Gère l'événement payment_intent.succeeded"""
    payment_intent_id = payment_intent.get('id')
    try:
        payment = PaymentRecord.objects.get(stripe_payment_intent_id=payment_intent_id)
        payment.status = 'completed'
        payment.save()
    except PaymentRecord.DoesNotExist:
        pass


def handle_payment_failed(payment_intent):
    """Gère l'événement payment_intent.payment_failed"""
    payment_intent_id = payment_intent.get('id')
    try:
        payment = PaymentRecord.objects.get(stripe_payment_intent_id=payment_intent_id)
        payment.status = 'failed'
        payment.save()
    except PaymentRecord.DoesNotExist:
        pass


def payment_history(request):
    """Historique des paiements"""
    payments = PaymentRecord.objects.all().order_by('-created_at')
    return render(request, 'payment_history.html', {'payments': payments})

