from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("checkout/<int:product_id>/", views.create_checkout_session, name="create_checkout"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("history/", views.payment_history, name="payment_history"),
    path("check-access/", views.check_access, name="check_access"),
    path("profile/", views.profile, name="profile"),
]
