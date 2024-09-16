from django.urls import path
# from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import MailingListView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailings_list'),
]