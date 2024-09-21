from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models

NULLABLE = {'blank': True, 'null': True}

PERIODICITY_CHOICES = [
    ('daily', 'Ежедневно'),
    ('weekly', 'Еженедельно'),
    ('monthly', 'Ежемесячно'),
]

STATUS_CHOICES = [
    ('created', 'Создана'),
    ('started', 'Запущена'),
    ('completed', 'Завершена'),
]


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Клиент')
    email = models.EmailField(verbose_name='Email', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'Клиент {self.email}({self.name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, help_text='Введите тему сообщения', verbose_name='Тема')
    content = models.TextField(help_text='Введите текст сообщения', verbose_name='Содержание')
    image = models.ImageField(upload_to="blogs/image", **NULLABLE, verbose_name="Изображение",
                              help_text="Загрузите изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    start_datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата и время начала рассылки",
                                          help_text="Введите дату и время начала рассылки", **NULLABLE)
    next_datetime = models.DateTimeField(verbose_name="Дата и время следующей отправки рассылки", **NULLABLE,
                                         editable=False)
    last_datetime = models.DateTimeField(verbose_name="Дата и время окончания рассылки",
                                         help_text="Введите дату и время окончания рассылки", **NULLABLE)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, verbose_name='Периодичность', **NULLABLE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение',
                                   related_name='mailings')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', related_name='mailings')

    def __str__(self):
        return f'Рассылка: "{self.message}" '

    def clean(self):
        if self.start_datetime and self.last_datetime and self.start_datetime >= self.last_datetime:
            raise ValidationError('Дата начала рассылки должна быть раньше даты окончания.')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='logs')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки рассылки", **NULLABLE)
    status = models.BooleanField(default=False, verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f'Попытка рассылки {self.mailing.pk}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
