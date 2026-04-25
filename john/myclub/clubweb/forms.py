from django import forms
from django.forms import ModelForm
from .models import Venue, MyClubuser, Event

# Create venue forms here.
#-----------------------------------------------------------------------------------------------------------

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = '__all__' # or ['name', 'address', 'zip_code', 'phone', 'web', 'email_address'] for specific fields 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the venue *'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address of the venue *'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zip code of the venue *'}),    
            'phone': forms.NumberInput (attrs={'class': 'form-control', 'placeholder': 'Phone number of the venue '}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'web address of the venue '}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address of the venue'}),
        }
#-----------------------------------------------------------------------------------------------------------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event # specify the model to use for this form
        fields =  ['name', 'event_date', 'venue', 'manager', 'attendees', 'description'] # specify the fields to include in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the event *'}),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Date of the event *'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue of the event *'}),
            'manager': forms.TextInput(attrs={'class': 'form-select', 'placeholder': 'Manager of the event *'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees of the event '}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of the event '}),
        }
#-----------------------------------------------------------------------------------------------------------

class MyClubuserForm(forms.ModelForm):
    class Meta:
        model = MyClubuser
        fields = '__all__'  