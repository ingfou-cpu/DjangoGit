from django.shortcuts import render
from .models import members


def home(request):
    all_members = members.objects.all
    return render(request, 'home.html', {'all': all_members})