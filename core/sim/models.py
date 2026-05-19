from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Modèle pour les produits à vendre"""
    name = models.CharField(max_length=255, help_text="Nom du produit")
    description = models.TextField(blank=True, help_text="Description du produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix en cents")
    stripe_price_id = models.CharField(max_length=255, help_text="ID du prix Stripe")
    stripe_product_id = models.CharField(max_length=255, blank=True, help_text="ID du produit Stripe")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return f"{self.name} - {self.price}€"


class CheckoutSessionRecord(models.Model):
    """Enregistrement des sessions de paiement"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="L'utilisateur qui a initié le checkout")
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_checkout_session_id = models.CharField(max_length=255, unique=True)
    stripe_price_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='eur')
    has_access = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Session de paiement"
        verbose_name_plural = "Sessions de paiement"
        ordering = ['-created_at']

    def __str__(self):
        return f"Checkout {self.stripe_checkout_session_id} - {self.user.username}"


class PaymentHistory(models.Model):
    """Historique des paiements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_session = models.ForeignKey(CheckoutSessionRecord, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='eur')
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100, blank=True)
    receipt_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique de paiement"
        verbose_name_plural = "Historique des paiements"
        ordering = ['-created_at']

    def __str__(self):
        return f"Paiement {self.stripe_payment_intent_id} - {self.amount}€"
