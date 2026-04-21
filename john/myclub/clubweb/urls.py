from django.urls import path, include
from . import views

app_name = 'clubweb'

urlpatterns = [
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique identifier
    path('', views.home, name='home'),
    path('<int:years>/<str:month>/', views.home, name='home'),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('events/', views.all_events, name='event_list'),
    ]
