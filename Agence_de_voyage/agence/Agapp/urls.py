from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('hotel/', views.Hotel, name='hotel'),
    path('reselieuChoisi/<int:destination_id>/', views.reselieuChoisi, name='reselieuChoisi'),
    path('about/', views.about, name='about'),
    path('croisiere/', views.croisiere, name='croisiere'),
    path('reservCroisiere/<int:pack_travel_id>/', views.reservCroisiere, name='reservCroisiere'),
    path('contact/', views.contact, name='contact'),
]