from django.contrib import admin
from .models import Product, CheckoutSessionRecord, PaymentHistory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stripe_price_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


@admin.register(CheckoutSessionRecord)
class CheckoutSessionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_checkout_session_id', 'product', 'amount_total', 'payment_status', 'is_completed', 'created_at')
    list_filter = ('payment_status', 'is_completed', 'has_access', 'created_at')
    search_fields = ('user__username', 'stripe_checkout_session_id')
    readonly_fields = ('stripe_checkout_session_id', 'stripe_customer_id')


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('user__username', 'stripe_payment_intent_id')
    readonly_fields = ('stripe_payment_intent_id', 'receipt_url')
