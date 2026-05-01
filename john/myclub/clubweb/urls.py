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
    #path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('<int:years>/<str:month>/', views.home, name='home'),
    path('events/', views.all_events, name='event_list'),
    path('add_venue/', views.add_venue, name='add_venue'),
    path('search_venues/', views.search_venues, name='search_venues'),
    path('venues/', views.venues, name='venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show_venue'), 
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/<event_id>', views.update_event, name='update_event'),
    path('update_venue/<venue_id>', views.update_venue, name='update_venue'),
    path('delete_event/<event_id>', views.delete_event, name='delete_event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete_venue'),
    path('venues_text_file/', views.venues_text_file, name='venues_text_file'),
    path('venues_csv_file/', views.venues_csv_file, name='venues_csv_file'),
    path('venues_pdf_file/', views.venues_pdf_file, name='venues_pdf_file'),
    path('paginate_events/', views.paginate_events, name='paginate_events'),
    ]
