import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Валидатор размера файлов (Максимум 5 МБ)
def validate_image_size(field_file_obj):
    megabyte_limit = 5
    if field_file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер фотографии — {megabyte_limit} МБ!")

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
    description = models.CharField(max_length=2000, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=9, 
        decimal_places=2, 
        verbose_name="Цена",
        validators=[MinValueValidator(0.01, message="Цена должна быть больше нуля!")]
    )
    
    # Добавлен валидатор размера и генерация пути по UUID
    image = models.ImageField(upload_to=get_main_photo_path, blank=True, null=True, validators=[validate_image_size])
    
    # Номер телефона храним в чистом виде (9 цифр: 555123456)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=30, verbose_name="Адрес", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='images', on_delete=models.CASCADE)
    # Добавлен валидатор размера
    image = models.ImageField(upload_to=get_gallery_photo_path, blank=True, null=True, validators=[validate_image_size])

    class Meta:
        verbose_name = "Фотография галереи"
        verbose_name_plural = "Фотографии галереи"


# --- СИГНАЛЫ ДЛЯ АВТОУДАЛЕНИЯ ФАЙЛОВ ИЗ DIGITALOCEAN SPACES ---

@receiver(post_delete, sender=Announcement)
def delete_main_image_on_announcement_delete(sender, instance, **kwargs):
    """Удаляет главное фото автоматически при удалении объявления"""
    if instance.image:
        try:
            # Универсальный метод django-storages: сам удалит и из DO Spaces, и с локалки
            instance.image.delete(save=False)
        except Exception as e:
            # Оборачиваем в try-except, чтобы даже если файл в облаке не нашелся, 
            # само объявление в БД успешно удалялось и пользователь не видел 500 ошибку
            print(f"Ошибка при удалении главного фото: {e}")

@receiver(post_delete, sender=AnnouncementImage)
def delete_gallery_image_on_announcement_image_delete(sender, instance, **kwargs):
    """Удаляет фото из галереи при удалении объекта фотографии"""
    if instance.image:
        try:
            instance.image.delete(save=False)
        except Exception as e:
            print(f"Ошибка при удалении фото галереи: {e}")