from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings

from anons.models import Announcement
from anons.forms import AnnouncementForm


def contacts(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        inquiry_type = request.POST.get('inquiry_type')
        source = request.POST.get('source')
        message = request.POST.get('message')

        full_message = f"""
        Новое сообщение от {first_name} {last_name}:

        Email: {email}
        Телефон: {phone}
        Тип запроса: {inquiry_type}
        Откуда узнал: {source}

        Сообщение:
        {message}
        """

        try:
            # Чистая, одиночная отправка без дублей
            send_mail(
                subject=f"Новая заявка: {inquiry_type}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['altaiabdurahim07@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Ваше сообщение успешно отправлено!")
            return redirect('contacts')
        except Exception as e:
            messages.error(request, f"Ошибка при отправке: {e}")
    
    return render(request, 'main/contacts.html')

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')


class Search(LoginRequiredMixin, ListView): 
    model = Announcement
    template_name = 'main/properties.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Announcement.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

def property_detail(request):
    return render(request, 'main/property_det.html')


@login_required
def create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES) 
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('properties')
    else:
        form = AnnouncementForm()
    return render(request, 'anons/create.html', {'form': form})