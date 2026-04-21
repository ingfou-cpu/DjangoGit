from django.contrib import admin

from .models import Venue, MyClubuser, Event

#admin.site.register(Venue)
admin.site.register(MyClubuser)
admin.site.register(Venue)
admin.site.register(Event)

"""# Register your models here.
#admin.site.register(clubweb)  
# Customizing the admin interface for Venue and clubweb models     
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone') 
    ordering = ('name',)
    search_fields = ('name', 'address') 
    
@admin.register(clubweb)    
class clubwebAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    search_fields = ('name', 'event_date')      """
    