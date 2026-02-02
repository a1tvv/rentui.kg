from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages

# Create your views here.



def contacts(request):
    if request.method == 'POST':
        # Сохраняем данные
        ContactMessage.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            inquiry_type=request.POST.get('inquiry_type'),
            source=request.POST.get('source'),
            message=request.POST.get('message'),
        )
        # Уведомление
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        # Редирект обратно на эту же страницу (имя из urls.py)
        return redirect('contacts') 

    # Если это просто заход на страницу (GET), показываем шаблон
    return render(request, 'main/contacts.html')


def home(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request,'main/about.html')

def properties(request):
    return render(request, 'main/properties.html')

def services(request):
    return render(request, 'main/services.html')

def property_detail(request):
    return render(request, 'main/property_det.html')