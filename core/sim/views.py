from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import stripe
import json
import logging

from .models import Product, CheckoutSessionRecord, PaymentHistory

logger = logging.getLogger(__name__)


def home(request):
    """Page d'accueil avec la liste des produits"""
    products = Product.objects.filter(is_active=True)
    context = {
        'products': products,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "home.html", context)


@login_required
def create_checkout_session(request, product_id):
    """Crée une session de paiement Stripe pour un produit"""
    if request.method != "POST":
        return redirect('home')
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Vérifier que l'utilisateur a un email valide
    user_email = request.user.email
    if not user_email:
        messages.error(request, "Veuillez configurer une adresse email valide dans votre profil avant de procéder au paiement.")
        return redirect('profile')
    
    # Validation approfondie de l'email
    try:
        validate_email(user_email)
    except ValidationError:
        messages.error(request, "Votre adresse email n'est pas valide. Veuillez la mettre à jour dans votre profil.")
        return redirect('profile')
    
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email,
            line_items=[
                {
                    "price": product.stripe_price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("cancel")),
            metadata={
                'user_id': request.user.id,
                'product_id': product.id,
            }
        )
        
        # Enregistrer la session dans la base de données
        CheckoutSessionRecord.objects.create(
            user=request.user,
            stripe_checkout_session_id=checkout_session.id,
            stripe_price_id=product.stripe_price_id,
            product=product,
            amount_total=product.price,
        )
        
        return redirect(checkout_session.url, code=303)
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        messages.error(request, f"Erreur de paiement: {str(e)}")
        return redirect('home')
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        messages.error(request, "Une erreur inattendue s'est produite.")
        return redirect('home')


def success(request):
    """Page de succès après un paiement"""
    session_id = request.GET.get('session_id')
    checkout_record = None
    
    if session_id:
        try:
            checkout_record = CheckoutSessionRecord.objects.get(
                stripe_checkout_session_id=session_id
            )
            checkout_record.is_completed = True
            checkout_record.has_access = True
            checkout_record.payment_status = 'completed'
            checkout_record.save()
        except CheckoutSessionRecord.DoesNotExist:
            logger.warning(f"Checkout session not found: {session_id}")
    
    return render(request, "success.html", {'checkout_record': checkout_record})


def cancel(request):
    """Page d'annulation de paiement"""
    return render(request, "cancel.html")


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
    
    # Gérer les événements
    event_type = event['type']
    logger.info(f"Received Stripe event: {event_type}")
    
    if event_type == 'checkout.session.completed':
        handle_checkout_session_completed(event['data']['object'])
    elif event_type == 'checkout.session.expired':
        handle_checkout_session_expired(event['data']['object'])
    elif event_type == 'payment_intent.succeeded':
        handle_payment_intent_succeeded(event['data']['object'])
    elif event_type == 'payment_intent.payment_failed':
        handle_payment_intent_failed(event['data']['object'])
    elif event_type == 'charge.refunded':
        handle_charge_refunded(event['data']['object'])
    
    return HttpResponse(status=200)


def handle_checkout_session_completed(session):
    """Gère l'événement checkout.session.completed"""
    session_id = session.get('id')
    
    try:
        checkout_record = CheckoutSessionRecord.objects.get(
            stripe_checkout_session_id=session_id
        )
        checkout_record.is_completed = True
        checkout_record.has_access = True
        checkout_record.payment_status = 'completed'
        checkout_record.stripe_customer_id = session.get('customer', '')
        checkout_record.amount_total = session.get('amount_total', 0) / 100
        checkout_record.save()
        
        logger.info(f"Checkout session completed: {session_id}")
        
    except CheckoutSessionRecord.DoesNotExist:
        logger.warning(f"Checkout session not found: {session_id}")


def handle_checkout_session_expired(session):
    """Gère l'événement checkout.session.expired"""
    session_id = session.get('id')
    
    try:
        checkout_record = CheckoutSessionRecord.objects.get(
            stripe_checkout_session_id=session_id
        )
        checkout_record.payment_status = 'expired'
        checkout_record.save()
        
        logger.info(f"Checkout session expired: {session_id}")
        
    except CheckoutSessionRecord.DoesNotExist:
        logger.warning(f"Checkout session not found: {session_id}")


def handle_payment_intent_succeeded(payment_intent):
    """Gère l'événement payment_intent.succeeded"""
    # Créer un enregistrement dans l'historique des paiements
    session_id = payment_intent.get('metadata', {}).get('session_id')
    
    if session_id:
        try:
            checkout_record = CheckoutSessionRecord.objects.get(
                stripe_checkout_session_id=session_id
            )
            
            PaymentHistory.objects.create(
                user=checkout_record.user,
                checkout_session=checkout_record,
                stripe_payment_intent_id=payment_intent.get('id'),
                amount=payment_intent.get('amount', 0) / 100,
                currency=payment_intent.get('currency', 'eur'),
                status='succeeded',
                payment_method=payment_intent.get('payment_method_types', [''])[0] if payment_intent.get('payment_method_types') else '',
                receipt_url=payment_intent.get('charges', {}).get('data', [{}])[0].get('receipt_url', '') if payment_intent.get('charges', {}).get('data') else '',
            )
            
            logger.info(f"Payment intent succeeded: {payment_intent.get('id')}")
            
        except CheckoutSessionRecord.DoesNotExist:
            logger.warning(f"Checkout session not found for payment: {session_id}")


def handle_payment_intent_failed(payment_intent):
    """Gère l'événement payment_intent.payment_failed"""
    session_id = payment_intent.get('metadata', {}).get('session_id')
    
    if session_id:
        try:
            checkout_record = CheckoutSessionRecord.objects.get(
                stripe_checkout_session_id=session_id
            )
            checkout_record.payment_status = 'failed'
            checkout_record.save()
            
            logger.info(f"Payment intent failed: {payment_intent.get('id')}")
            
        except CheckoutSessionRecord.DoesNotExist:
            logger.warning(f"Checkout session not found for failed payment: {session_id}")


def handle_charge_refunded(charge):
    """Gère l'événement charge.refunded"""
    payment_intent_id = charge.get('payment_intent')
    
    if payment_intent_id:
        try:
            payment_history = PaymentHistory.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            payment_history.status = 'refunded'
            payment_history.save()
            
            # Mettre à jour le checkout record
            checkout_record = payment_history.checkout_session
            checkout_record.has_access = False
            checkout_record.save()
            
            logger.info(f"Charge refunded: {charge.get('id')}")
            
        except PaymentHistory.DoesNotExist:
            logger.warning(f"Payment history not found for refund: {payment_intent_id}")


@login_required
def payment_history(request):
    """Affiche l'historique des paiements de l'utilisateur"""
    payments = PaymentHistory.objects.filter(user=request.user)
    return render(request, "payment_history.html", {'payments': payments})


@login_required
def check_access(request):
    """Vérifie si l'utilisateur a accès au contenu payant"""
    has_access = CheckoutSessionRecord.objects.filter(
        user=request.user,
        has_access=True,
        is_completed=True
    ).exists()
    
    return JsonResponse({'has_access': has_access})


@login_required
def profile(request):
    """Page de profil utilisateur pour gérer l'email"""
    user = request.user
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        # Validation de l'email
        if not email:
            messages.error(request, "L'adresse email est obligatoire.")
        else:
            try:
                validate_email(email)
                # Vérifier si l'email est déjà utilisé par un autre utilisateur
                if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                    messages.error(request, "Cette adresse email est déjà utilisée par un autre compte.")
                else:
                    user.email = email
                    user.save()
                    messages.success(request, "Votre adresse email a été mise à jour avec succès.")
                    return redirect('profile')
            except ValidationError:
                messages.error(request, "Veuillez entrer une adresse email valide.")
    
    # Vérifier si l'email est valide
    email_valid = False
    if user.email:
        try:
            validate_email(user.email)
            email_valid = True
        except ValidationError:
            pass
    
    context = {
        'user': user,
        'email_valid': email_valid,
    }
    return render(request, "profile.html", context)
