from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("email", views.send_email_view, name="email"),
    path("verify/<uuid:token>", views.verify_email, name="verify_email"),
]
