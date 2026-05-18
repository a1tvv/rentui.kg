import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Функции для генерации уникальных имён на латинице (UUID)
def get_main_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    return os.path.join('main_photos', unique_name)

def get_gallery_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    return os.path.join('gallery', unique_name)


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.CharField(max_length=255, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=7, 
        decimal_places=2, 
        verbose_name="Цена",
        validators=[MinValueValidator(0.01, message="Цена должна быть больше нуля!")]
    )
    
    image = models.ImageField(upload_to='anonc-img/', blank=True, null=True)
    
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", default="+996 ")
    address = models.CharField(max_length=30, verbose_name="Город", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='images', on_delete=models.CASCADE)
    
    # И ДЛЯ ГАЛЕРЕИ ТОЖЕ ПОДКЛЮЧИЛИ:
    image = models.ImageField(upload_to=get_gallery_photo_path, blank=True, null=True)

    class Meta:
        verbose_name = "Фотография галереи"
        verbose_name_plural = "Фотографии галереи"