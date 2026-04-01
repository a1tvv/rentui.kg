from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import ListView

from anons.models import Announcement
from anons.forms import AnnouncementForm

# Create your views here.

def contacts(request):
    if request.method == 'POST':
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
    return render(request, 'main/contacts.html')

def home(request):
    return render(request, 'base.html')

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

