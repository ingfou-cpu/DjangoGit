from django.shortcuts import render,redirect
from .models import Member
from .forms import MemberForm   
from django.contrib import messages

def form(request):
    return render(request, 'form.html')

def home(request):
    all_members = Member.objects.all()
    return render(request, 'home.html', {'all': all_members})

def join(request):
    if request.method == 'POST':
        form = MemberForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'join.html', {'form': form})
        messages.success(request, 'Your form has been submitted successfully!')
        return redirect('home')         
    else:
        form = MemberForm()
    return render(request, 'join.html', {'form': form})

"""def join(request):
    if request.method == 'POST':
        name = request.POST['name']
        lname = request.POST['lname']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        member = Member(name=name, lname=lname, age=age, email=email, phone=phone, address=address)
        member.save()
    return render(request, 'join.html')"""
