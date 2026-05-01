# User Registration with Email Confirmation - Setup Guide

## Features Implemented

✅ User registration with form validation
✅ Email verification with unique tokens
✅ 24-hour token expiration
✅ User account activation on email verification
✅ Login/Logout functionality
✅ Bootstrap 5 UI
✅ Admin panel integration
✅ Error handling and user messages

## Setup Steps

### 1. Create Database Migrations

Run these commands in the project directory:

```bash
python manage.py makemigrations clubweb
python manage.py migrate
```

### 2. Email Configuration (Development)

The project is configured to use **Console Email Backend** for development. 
Emails will be printed to the console instead of being sent.

For **Production**, update `myclub/settings.py`:

```python
# Gmail SMTP Example
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use app-specific password
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

- **Home Page**: http://localhost:8000/
- **Register**: http://localhost:8000/register/
- **Login**: http://localhost:8000/login/
- **Admin Panel**: http://localhost:8000/admin/

## User Registration Flow

1. User fills out registration form with:
   - Username
   - Email
   - First Name (optional)
   - Last Name (optional)
   - Password
   - Password Confirmation

2. System creates user account (initially inactive) and UserProfile
3. System generates unique email verification token
4. Verification email is sent with a 24-hour validity link
5. User clicks link in email to verify
6. User account is activated
7. User can now login

## File Structure

```
clubweb/
├── models.py                    # UserProfile model
├── forms.py                     # RegistrationForm
├── views.py                     # All view functions
├── urls.py                      # URL routing
├── admin.py                     # Admin configuration
└── templates/
    └── clubweb/
        ├── base.html            # Base template with navbar
        ├── register.html        # Registration form
        ├── login.html           # Login form
        └── home.html            # Home page
```

## Testing

### Manual Testing
1. Go to http://localhost:8000/register/
2. Fill in the form and submit
3. Check Django console for verification email
4. Copy the verification link
5. Paste and visit the link in browser
6. Account should be verified
7. Try logging in

### Test Account
```
Username: testuser
Email: test@example.com
Password: TestPass123!
```

## Troubleshooting

**Issue**: UserProfile not created automatically
- **Solution**: Run migrations: `python manage.py migrate`

**Issue**: Email not sending
- **Solution**: Check console output for email content (development mode)
- For production, verify SMTP credentials in settings.py

**Issue**: Verification link expired
- **Solution**: User can register again to get a new link

## Security Notes

- Tokens are unique UUIDs (strong randomization)
- Tokens expire after 24 hours
- Passwords are hashed using Django's default PBKDF2
- CSRF protection enabled on all forms
- Email validation on registration form

## Next Steps

You can extend this system with:
- Password reset functionality
- Email resend capability
- Social authentication (Google, Facebook)
- Two-factor authentication
- User profile customization
- Role-based permissions

## Support

For issues or questions, check:
1. Django documentation: https://docs.djangoproject.com/
2. Django email documentation: https://docs.djangoproject.com/en/stable/topics/email/
3. Console output for debugging information
