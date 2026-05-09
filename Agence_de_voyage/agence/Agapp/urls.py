from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('hotel/', views.Hotel, name='hotel'),
    path('reselieuChoisi/<int:destination_id>/', views.reselieuChoisi, name='reselieuChoisi'),
]