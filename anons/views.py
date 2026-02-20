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

@login_required
def property_delete(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)
    
    if property_item.author == request.user:
        property_item.delete()
        messages.success(request, "Объявление удалено.")
    else:
        messages.error(request, "Вы не можете удалить чужое объявление.")
        
    return redirect('properties')

@login_required 
def create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            
            # Устанавливаем главное фото из первого выбранного
            if files:
                announcement.image = files[0]
            
            announcement.save()

            # Сохраняем все фото в галерею
            for f in files:
                AnnouncementImage.objects.create(announcement=announcement, image=f)
            
            messages.success(request, "Объявление успешно создано!")
            return redirect('home')
        else:
            # Если форма невалидна, Django сам вернет ошибки в шаблон через {{ form.errors }}
            messages.error(request, "Проверьте правильность заполнения полей.")
    else:
        form = AnnouncementForm()
    
    return render(request, 'anons/create.html', {'form': form})


@login_required
def property_edit(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)
    
    if property_item.author != request.user:
        messages.error(request, "У вас нет прав на редактирование.")
        return redirect('home')

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=property_item)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            announcement = form.save(commit=False)
            
            if files:
                # Если загружены новые фото, меняем главное фото
                announcement.image = files[0]
                # ОПЦИОНАЛЬНО: Удаляем старые фото из галереи перед добавлением новых
                # announcement.images.all().delete() 
                
                announcement.save() # Сначала сохраняем основную модель

                for f in files:
                    AnnouncementImage.objects.create(announcement=announcement, image=f)
            else:
                announcement.save()

            messages.success(request, "Объявление обновлено!")
            return redirect('home')
    else:
        form = AnnouncementForm(instance=property_item)
    
    # Передаем сам объект, чтобы в шаблоне вывести уже существующие фото
    return render(request, 'anons/create.html', {
        'form': form, 
        'edit_mode': True, 
        'property_item': property_item
    })