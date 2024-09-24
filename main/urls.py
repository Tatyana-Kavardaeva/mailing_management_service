from django.urls import path
# from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    ContactPageView, MainPageView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MakeMailingView, get_mailinglog_view

app_name = MainConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('make_mailing/', MakeMailingView.as_view(), name='make_mailing'),

    path('mailings_list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('clients_list/', ClientListView.as_view(), name='clients_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('logs_list/', get_mailinglog_view, name='logs_list'),

    path('contact/', ContactPageView.as_view(), name='contact')
]
