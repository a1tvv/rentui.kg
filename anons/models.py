from django.db import models

from django.contrib.auth.models import User # Импортируем встроенных юзеров

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, verbose_name="Цена")
    image = models.ImageField("Главное фото", upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", default="+996 ")
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    # Связь: один пользователь может иметь много записей
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    
class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='announcements/gallery/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"