from django.contrib import admin
from .models import Destination, Hotel, Booking, Contact, Testimonial, pack_travel
# Register your models here.

admin.site.register(Destination)   
admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Contact)
admin.site.register(Testimonial)
admin.site.register(pack_travel)

