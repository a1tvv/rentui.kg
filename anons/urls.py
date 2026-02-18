from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='sign-up'),
    path('create/', views.create, name='create-anons'),
    path('user_login/', views.user_login, name='login'),
    path('create/', views.create, name='create-anons'),
    path('property/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
]
