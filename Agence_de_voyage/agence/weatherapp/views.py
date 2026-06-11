from django.shortcuts import render, redirect
import requests
from .models import SearchHistory
# Create your views here.


API_KEY = "4d7e013edeb48f3561ed2c988b3cfaf1"


def get_weather_for_city(city_name):
    """Récupère les données météo pour une ville donnée.
    Retourne un dict avec les données météo ou None en cas d'erreur."""
    if not city_name:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            return {
                'city': f"{data['name']}, {data['sys']['country']}",
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
            }
    except requests.RequestException:
        pass
    return None


def index(request):
    weather = None
    error = None
    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]

    if request.method == "POST":
        city = request.POST.get('city', '').strip()
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                resp = requests.get(url, timeout=5)
                data = resp.json()

                if resp.status_code == 200:
                    weather = {
                        'city': f"{data['name']}, {data['sys']['country']}",
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon'],
                    }
                    SearchHistory.objects.create(
                        city_name=data['name'],
                        temperature=data['main']['temp'],
                        humidity=data['main']['humidity'],
                        pressure=data['main']['pressure'],
                        description=data['weather'][0]['description'].title()
                    )
                    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
                else:
                    error = data.get("message", "Could not fetch weather data.")
            except requests.RequestException:
                error = "Network error. Please try again."
        else:
            error = "Please enter a city name."
    
    # Si la requête vient de home, sauvegarder en session et rediriger
    if request.POST.get('from_home'):
        request.session['weather_data'] = weather
        request.session['weather_error'] = error
        return redirect('home')

    return render(request, "index.html", {
        'weather': weather,
        'error': error,
        'recent_searches': recent_searches
    })