from time import sleep
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Рассылки'

    # def ready(self):
    #     from main.services import start_mailing
    #     sleep(2)
    #     start_mailing()
