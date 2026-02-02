from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import AnnouncementForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'anons/sign-up.html', {'form': form})


@login_required # Только залогиненные могут добавлять
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user 
            announcement.save()
            return redirect('home')
    else:
        form = AnnouncementForm()
    return render(request, 'anons/create.html', {'form': form})