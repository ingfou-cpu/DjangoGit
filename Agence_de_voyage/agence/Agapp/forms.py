from django.db import models
from django import forms
from django.forms import ModelForm
from .models import  Contact

"""class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }"""

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields =('name','phone', 'email', 'message')