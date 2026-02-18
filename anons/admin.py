from django.contrib import admin
from .models import Announcement, AnnouncementImage

class AnnouncementImageInline(admin.TabularInline):
    model = AnnouncementImage
    extra = 3  # Количество пустых слотов для фото по умолчанию

@admin.register(Announcement) # <--- Вот этот декоратор УЖЕ регистрирует модель
class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [AnnouncementImageInline]
    list_display = ('title', 'price', 'author', 'created_at')