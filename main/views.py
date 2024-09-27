import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from blog.models import Post
from main.form import MailingForm, ClientForm, MessageForm, MailingManagerForm
from main.models import Mailing, Client, Message, MailingLog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from main.services import send_mailing
from django.core.exceptions import PermissionDenied


class OwnerPermissionMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class ManagerPermissionMixin:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)

        if user.has_perm('main.set_active_status'):
            return queryset
        return queryset.filter(owner=user)


class FormValidMixin:
    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class ClientListView(ManagerPermissionMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()
        return context


class ClientDetailView(OwnerPermissionMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:make_mailing')

class ClientUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(OwnerPermissionMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:clients_list')


class MessageListView(ManagerPermissionMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()
        return context


class MessageDetailView(OwnerPermissionMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('main:messages_list')


class MessageUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('main:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(OwnerPermissionMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:messages_list')


class MailingListView(ManagerPermissionMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()
        # context['mailings'] = get_mailings_from_cache()
        return context


class MailingDetailView(DetailView):
    model = Mailing

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        send_mailing(mailing)
        logs = MailingLog.objects.filter(mailing=mailing).order_by('-sent_at')

        if logs:
            messages.success(request, 'Рассылка завершена')
        else:
            messages.error(request, 'Не удалось выполнить рассылку. Проверьте настройки.')

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        mailing = self.get_object()
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        context['clients'] = mailing.clients.all()
        logs = MailingLog.objects.filter(mailing=self.object).order_by(
            '-sent_at')
        context['last_log'] = mailing.logs.first()
        context['user'] = mailing.owner
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()
        return context

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])


class MailingCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.object.pk])


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('main.set_active_status'):
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(OwnerPermissionMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailings_list')


def get_mailinglog_view(request):
    user = request.user
    if user.has_perm('main.set_active_status'):
        mailing_logs = MailingLog.objects.all()
    elif user.is_authenticated:
        mailing_logs = MailingLog.objects.filter(owner=request.user)
    else:
        mailing_logs = Mailing.objects.none()
    return render(request, 'main/mailinglog_list.html', {'object_list': mailing_logs})


class ContactPageView(TemplateView):
    template_name = 'main/contact.html'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'main/contact.html')


class MainPageView(TemplateView):
    def get_template_names(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return ['main/main_manager_page.html']
        return ['main/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(is_published=True)
        random_posts = random.sample(list(posts), min(3, len(posts)))
        context['random_posts'] = random_posts
        if self.request.user.is_authenticated:
            context['mailing_count'] = Mailing.objects.filter(owner=self.request.user).count()
            active_mailing_count = Mailing.objects.filter(status__in=['created', 'started'])
            context['active_mailing_count'] = active_mailing_count.filter(owner=self.request.user).count()
            context['clients_count'] = Client.objects.filter(owner=self.request.user).count()
            context['user_email'] = self.request.user.email

        return context


class MakeMailingView(TemplateView):
    template_name = 'main/make_mailing.html'
