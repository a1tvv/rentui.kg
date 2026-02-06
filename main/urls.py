from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('properties/', views.properties, name='properties'),
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),
    path('property_detail/', views.property_detail, name='property_detail'),
    path('create', views.create, name='create')
]