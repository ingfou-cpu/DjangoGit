from django.contrib import admin
from .models import Venue, MyClubuser, Event

admin.site.register(Venue)
admin.site.register(MyClubuser)
admin.site.register(Event)


"""
# Customizing the admin interface for Venue and clubweb models     
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Venue details', {
            'fields': ('name', 'address', 'zip_code')
        }),
        ('Contact information', {
            'fields': ('phone', 'web', 'email_address')
        }),
    )
    list_display = ('name', 'address', 'phone') 
    ordering = ('-name',)
    search_fields = ('name', 'address') 
    model = Venue
    extra = 0

@admin.register(Event)    
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    search_fields = ('name', 'event_date') 

# Register your models here.
#     """
    