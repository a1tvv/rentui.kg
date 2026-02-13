from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import Announcement
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


def create(request):
    if request.method == 'POST':
        form = Announcement(request.POST, request.FILES)
        
        if form.is_valid():
            announcement = form.save(commit=False)

            if request.user.is_authenticated:
                announcement.author = request.user
                
            announcement.save()
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.author = request.user
                announcement.save()
            return redirect('home')
    else:
        form = Announcement()
    
    # Обязательно передаем объект form в контекст шаблона!
    return render(request, 'anons/create.html', {'form': form})

@login_required # Только залогиненные могут добавлять
def create_announcement(request):
    if request.method == 'POST':
        form = Announcement(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user 
            announcement.save()
            return redirect('home')
    else:
        form = Announcement()
    return render(request, 'anons/create.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в аккаунт!")
            return redirect('home')
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()

    return render(request, 'anons/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return redirect('home')