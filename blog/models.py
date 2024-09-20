from django.db import models
from main.models import NULLABLE


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    body = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to="blogs/image", **NULLABLE, verbose_name="Изображение",
                              help_text="Загрузите изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", help_text="Введите дату")
    view_counter = models.PositiveIntegerField(verbose_name="Просмотры", default=0)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
