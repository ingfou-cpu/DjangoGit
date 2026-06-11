# Test from the python shell

python3 manage.py shell

from django.core.mail import send_mail

from django.conf import settings


send_mail(
    'Test Email',
    'If you receive this, SSL works!',
    settings.EMAIL_HOST_USER,
    ['your_email@gmail.com'],
    fail_silently=False
)


# if facing issue

SSL: CERTIFICATE_VERIFY_FAILED

# Run this command in the terminal

/Applications/Python\ 3.13/Install\ Certificates.command
