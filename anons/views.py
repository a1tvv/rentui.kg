from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AnnouncementForm
from .models import AnnouncementImage, Announcement
from django.core.paginator import Paginator
from django.db.models import Q


# --- РЕГИСТРАЦИЯ И ВХОД ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('properties')
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
            return redirect('properties')
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
    property_item = Announcement.objects.filter(pk=pk).first()

    if not property_item:
        return redirect('properties')

    if property_item.author == request.user or request.user.is_superuser:
        property_item.delete()
        messages.success(request, "Объявление успешно удалено.")
    else:
        messages.error(request, "У вас нет прав на удаление этого объявления.")

    return redirect('properties')

@login_required
def create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        images = request.FILES.getlist('images')

        print("ВСЕ КЛЮЧИ FILES:", dict(request.FILES))
        print("ПОЛУЧЕНО ФАЙЛОВ:", len(images))

        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user

            if images:
                announcement.image = images[0]

            announcement.save()

            for f in images[1:]:
                AnnouncementImage.objects.create(announcement=announcement, image=f)

            messages.success(request, "Объявление успешно создано!")
            return redirect('home')
        else:
            messages.error(request, "Проверьте правильность заполнения полей.")
    else:
        form = AnnouncementForm()

    return render(request, 'anons/create.html', {'form': form})
@login_required
def property_edit(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)

    if property_item.author != request.user and not request.user.is_superuser:
        messages.error(request, "У вас нет прав на редактирование.")
        return redirect('home')

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=property_item)
        images = request.FILES.getlist('images')

        if form.is_valid():
            announcement = form.save(commit=False)

            if images:
                announcement.image = images[0]   # заменяем главное фото

            announcement.save()

            for f in images[1:]:                 # доливаем в галерею
                AnnouncementImage.objects.create(announcement=announcement, image=f)

            messages.success(request, "Объявление обновлено!")
            return redirect('home')
    else:
        form = AnnouncementForm(instance=property_item)

    return render(request, 'anons/create.html', {
        'form': form,
        'edit_mode': True,
        'property_item': property_item
    })


def property_list(request):
    announcements_list = Announcement.objects.select_related('author').all().order_by('-id')

    search_query = request.GET.get('search')
    if search_query:
        announcements_list = announcements_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(announcements_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'anons/property_list.html', {'page_obj': page_obj})