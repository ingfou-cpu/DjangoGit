from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .forms import RegistrationForm
from .models import UserProfile

# Create your views here.
def home(request):
    return render(request, 'home.html', {'title': 'Home'})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email is verified
            user.save()
            
            profile = user.profile
            # Generate verification token
            profile.generate_token()
            profile.token_created_at = timezone.now()
            profile.save()
            
            # Send verification email
            try:
                send_verification_email(user, request)
                messages.success(request, 'Registration successful! Please check your email to verify your account.')
                return redirect('authen:login')
            except Exception as e:
                # If email fails, delete profile first to avoid FK constraint issues,
                # then delete the user.
                try:
                    user.profile.delete()
                except Exception:
                    pass
                user.delete()
                messages.error(request, f'Registration error: {str(e)}. Please try again.')
                return render(request, 'authen/register.html', {'form': form})
    else:
        form = RegistrationForm()
    
    return render(request, 'authen/register.html', {'form': form})

def verify_email(request, token):
    try:
        profile = UserProfile.objects.get(email_verification_token=token)
        
        # Check if token is still valid (24 hours)
        if profile.token_created_at and (timezone.now() - profile.token_created_at) > timedelta(hours=24):
            messages.error(request, 'Verification link has expired. Please register again.')
            profile.user.delete()
            return redirect('authen:register')
        
        # Mark email as verified
        profile.email_verified = True
        profile.email_verification_token = None
        profile.save()
        
        # Activate user
        user = profile.user
        user.is_active = True
        user.save()
        
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('authen:register')
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('authen:register')

def send_verification_email(user, request):
    profile = user.profile
    verification_link = request.build_absolute_uri(
        reverse('authen:verify_email', kwargs={'token': profile.email_verification_token})
    )
    
    subject = 'Verify Your Email - MyClub Registration'
    message = f"""
    Hello {user.first_name or user.username},

    Thank you for registering with MyClub! Please verify your email by clicking the link below:

    {verification_link}

    This link will expire in 24 hours.

    If you did not create this account, please ignore this email.

    Best regards,
    MyClub Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    print(f"✅ VERIFICATION EMAIL SENT TO: {user.email}")
    print(f"🔗 VERIFICATION LINK: {verification_link}")
    print("=" * 50)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('authen:home')
            else:
                messages.error(request, 'Your account is not activated. Please verify your email.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authen/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authen:home')
    