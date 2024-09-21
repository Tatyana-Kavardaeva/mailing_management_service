import smtplib
import datetime
from time import sleep
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config import settings


def send_mailing(mailing):
    """Функция для рассылки клиентам"""
    from main.models import Mailing, MailingLog
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)

    mailings = Mailing.objects.all()

    for mailing in mailings:
        # проверяем не наступил ли срок окончания рассылки
        if mailing.last_datetime is not None and mailing.last_datetime <= current_datetime:
            mailing.status = 'completed'
            mailing.save()

        # проверяем закончился ли период между рассылками
        mailing_log = MailingLog.objects.filter(mailing=mailing).order_by('-sent_at').first()
        if mailing_log:
            time_delta = current_datetime - mailing_log.sent_at

            if mailing.periodicity == "daily" and time_delta.days >= 1:
                mailing.next_datetime = mailing_log.sent_at + datetime.timedelta(days=1)
                mailing.status = 'started'
                mailing.save()
            elif mailing.periodicity == "weekly" and time_delta.days >= 7:
                mailing.next_datetime = mailing_log.sent_at + datetime.timedelta(weeks=1)
                mailing.status = 'started'
                mailing.save()
            elif mailing.periodicity == "monthly" and time_delta.days >= 30:
                mailing.next_datetime = mailing_log.sent_at + datetime.timedelta(days=30)
                mailing.status = 'started'
                mailing.save()

    mailings = Mailing.objects.filter(start_datetime__lte=current_datetime, status__in=['created', 'started'])

    if not mailings.exists():
        print("Нет рассылок готовых к отправке")

    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.title,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()] + [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            mailing.status = 'started'
            mailing.save()

            MailingLog.objects.create(mailing=mailing, status=True, response='Рассылка успешно отправлена')

            print(f"{mailing} успешно отправлена")

        except smtplib.SMTPException as e:
            MailingLog.objects.create(mailing=mailing, status=False, response=str(e))
            print(f"Ошибка при отправке {mailing}: {e}")

    if mailing.last_datetime is None:
        mailing.status = 'completed'
        mailing.save()


def start_mailing():
    """Запускает рассылки клиентам"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()

    while True:
        sleep(1)
