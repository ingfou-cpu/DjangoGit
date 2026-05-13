from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('reselieuChoisi/<int:destination_id>/', views.reselieuChoisi, name='reselieuChoisi'),

]



"""
path('hotel/', views.Hotel, name='hotel'),
path('croisiere/', views.croisiere, name='croisiere'),
path('reservCroisiere/<int:pack_travel_id>/', views.reservCroisiere, name='reservCroisiere'),"""