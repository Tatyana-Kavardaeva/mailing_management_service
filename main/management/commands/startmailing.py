from django.core.management import BaseCommand
from main.services import start_mailing


class Command(BaseCommand):
    """Команда для запуска рассылок клиентам"""

    def handle(self, *args, **options):
        start_mailing()
