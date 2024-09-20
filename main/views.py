import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from blog.models import Post
from main.form import MailingForm, ClientForm, MessageForm, MailingLogForm
from main.models import Mailing, Client, Message, MailingLog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from main.services import send_mailing


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:make_mailing')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:clients_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('main:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('main:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:messages_list')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        send_mailing(mailing)
        MailingLog.objects.create(mailing=mailing, status=True, response="Рассылка успешно отправлена")
        messages.success(request, 'Рассылка успешно отправлена!')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        mailing = self.get_object()
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        context['clients'] = mailing.clients.all()
        context['logs'] = MailingLog.objects.filter(mailing=self.object).order_by(
            '-sent_at')
        context['logs'] = mailing.logs.first()
        print(context['clients'])
        print(context['logs'])
        return context

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.object.pk])
    # success_url = reverse_lazy('main:mailings_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailings_list')


class MailingLogListView(ListView):
    model = MailingLog


class MailingLogDetailView(DetailView):
    model = MailingLog


class MailingLogCreateView(CreateView):
    model = MailingLog
    form_class = MailingLogForm
    success_url = reverse_lazy('main:mailings_list')


class MailingLogUpdateView(UpdateView):
    model = MailingLog
    form_class = MailingLogForm

    def get_success_url(self):
        return reverse('main:log_detail', args=[self.kwargs.get('pk')])


class MailingLogDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:logs_list')


class ContactPageView(TemplateView):
    template_name = "main/contact.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f'You have new message from {name}({phone}): {message}')
        return render(request, "main/contact.html")


class MainPageView(TemplateView):
    template_name = 'main/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(is_published=True)
        random_posts = random.sample(list(posts), min(3, len(posts)))
        context['random_posts'] = random_posts
        return context


class MakeMailingView(TemplateView):
    template_name = 'main/make_mailing.html'
