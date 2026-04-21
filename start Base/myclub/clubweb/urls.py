from django.urls import path, include
from . import views

app_name = 'clubweb'

urlpatterns = [
    path('', views.home, name='home'),
]
