from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .models import EmailVerification

def home(request):
    return render(request, "home.html")

def send_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Create verification instance
            verification = EmailVerification.objects.create(email=email)
            
            # Send verification email
            subject = "Verify Your Email"
            verification_url = request.build_absolute_uri(reverse('verify_email', args=[verification.token]))
            message = f"Please click the link to verify your email: {verification_url}"
            recipient_list = [email]

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=True,
            )
            messages.success(request, 'Verification email sent!')
        else:
            messages.error(request, 'Please provide an email address.')
    return render(request, "home.html")

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token, is_verified=False)
        verification.is_verified = True
        verification.save()
        messages.success(request, 'Email verified successfully!')
        return redirect('home')  # Assuming you have a home view
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('home')