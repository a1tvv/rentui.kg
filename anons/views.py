from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AnnouncementForm 
from .models import AnnouncementImage, Announcement

# --- РЕГИСТРАЦИЯ И ВХОД ---
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

# --- ОСНОВНЫЕ ФУНКЦИИ ---

@login_required 
def create(request):
    if request.method == 'POST':
        # Передаем request.FILES, чтобы Django увидел файлы
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            
            # Получаем список файлов из поля 'image'
            files = request.FILES.getlist('image')
            
            if files:
                # Назначаем первый файл как главное фото объявления
                announcement.image = files[0]
            
            announcement.save() # Сначала сохраняем само объявление

            # Теперь сохраняем все файлы (включая первый) в модель доп. изображений
            for f in files:
                AnnouncementImage.objects.create(
                    announcement=announcement, 
                    image=f
                )
            
            messages.success(request, "Успешно создано!")
            return redirect('home')
    else:
        form = AnnouncementForm()
    return render(request, 'anons/create.html', {'form': form})


@login_required
def property_edit(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)
    
    if property_item.author != request.user:
        messages.error(request, "У вас нет прав...")
        return redirect('home')

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=property_item)
        if form.is_valid():
            announcement = form.save() # Сохраняем основные данные
            
            # Обработка новых фото при редактировании
            files = request.FILES.getlist('image')
            if files:
                # Если загрузили новые, можно либо очистить старые, либо просто добавить
                for f in files:
                    AnnouncementImage.objects.create(announcement=announcement, image=f)
            
            messages.success(request, "Объявление обновлено!")
            return redirect('home')
    else:
        form = AnnouncementForm(instance=property_item)
    
    return render(request, 'anons/create.html', {'form': form, 'edit_mode': True})

@login_required
def property_delete(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)
    
    if property_item.author == request.user:
        property_item.delete()
        messages.success(request, "Объявление удалено.")
    else:
        messages.error(request, "Вы не можете удалить чужое объявление.")
        
    return redirect('properties')