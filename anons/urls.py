from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='sign-up'),
    path('create/', views.create, name='create-anons'),
    path('user_login/', views.user_login, name='login')
]
