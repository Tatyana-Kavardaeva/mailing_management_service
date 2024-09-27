from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=50, verbose_name='Телефон', **NULLABLE,
                             help_text='Введите номер телефона')
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE,
                               help_text='Введите страну проживания')
    avatar = models.ImageField(upload_to='users/avatars', **NULLABLE, verbose_name='Аватар',
                               help_text='Загрузите свой аватар')
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('set_active_user', 'Can active user'),
            ('set_viewing_user', 'Can viewing user')
        ]

    def __str__(self):
        return self.email
