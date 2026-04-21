from django.contrib import admin
from store.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created')
    prepopulated_fields = {'slug': ('name',)}
