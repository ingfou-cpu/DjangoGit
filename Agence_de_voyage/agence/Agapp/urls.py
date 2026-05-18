from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('circuit/', views.circuit, name='circuit'),
    path('reselieuChoisi/<int:destination_id>/', views.reselieuChoisi, name='reselieuChoisi'),
    path('circuitChoisi/<int:pack_travel_id>/', views.circuitChoisi, name='circuitChoisi'),
    path('reservCroisiere/<int:pack_travel_id>/', views.reservCroisiere, name='reservCroisiere'),
]
