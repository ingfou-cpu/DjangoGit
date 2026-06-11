from django.contrib import admin
from .models import Item
# Register your models here.

admin.site.register(Item)
# To customize the admin interface for the Item model, you can create a ModelAdmin class. For example:
