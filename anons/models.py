from django.db import models

from django.contrib.auth.models import User # Импортируем встроенных юзеров

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='announcements/', verbose_name="Фото", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Связь: один пользователь может иметь много записей
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title