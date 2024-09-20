from django.apps import AppConfig
from main.services import start_mailing


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Рассылки'
    #
    # def ready(self):
    #     start_mailing()
