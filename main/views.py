from django.shortcuts import render, redirect
from django.contrib import messages
from anons.models import Announcement
from django.contrib.auth.decorators import login_required
from anons.forms import AnnouncementForm

# Create your views here.



def contacts(request):
    if request.method == 'POST':
        # Сохраняем данные
        Announcement.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            inquiry_type=request.POST.get('inquiry_type'),
            source=request.POST.get('source'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('contacts') 

    # Если это просто заход на страницу (GET), показываем шаблон
    return render(request, 'main/contacts.html')


def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request,'main/about.html')

def services(request):
    return render(request, 'main/services.html')

@login_required
def properties(request): 
    anons = Announcement.objects.all()
    return render(request, 'main/properties.html', {'anons': anons})

def property_detail(request):
    return render(request, 'main/property_det.html')


@login_required
def create(request):
    if request.method == 'POST':
        # Передаем данные из запроса в форму
        form = AnnouncementForm(request.POST, request.FILES) 
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user # Привязываем автора
            announcement.save()
            return redirect('properties')
    else:
        form = AnnouncementForm() # Создаем пустую форму для GET запроса
    
    return render(request, 'anons/create.html', {'form': form})