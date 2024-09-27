import smtplib
import datetime
from time import sleep
import pytz
from django.core.mail import send_mail
from config import settings
from main.models import MailingLog


def send_mailing(mailing):
    """Функция для рассылки клиентам"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)

    # Проверяем, была ли отправка ранее
    mailing_log = MailingLog.objects.filter(mailing=mailing).order_by('-sent_at').first()

    # Если last_datetime не указана, отправляем рассылку один раз
    if mailing.last_datetime is None:
        if mailing.status in ['created', 'started'] and mailing.start_datetime <= current_datetime:
            try:
                send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()] + [settings.EMAIL_HOST_USER],
                    fail_silently=False
                )
                mailing.status = 'completed'  # Меняем статус на завершено после отправки
                mailing.save()

                MailingLog.objects.create(mailing=mailing, status=True, response='Рассылка успешно отправлена')
                print(f"{mailing} успешно отправлена")

            except smtplib.SMTPException as e:
                MailingLog.objects.create(mailing=mailing, status=False, response=str(e))
                print(f"Ошибка при отправке {mailing}: {e}")
        return  # Завершаем выполнение функции, так как рассылка завершена

    # Проверяем не наступил ли срок окончания рассылки
    if mailing.last_datetime is not None and mailing.last_datetime <= current_datetime:
        if mailing.status != 'completed':
            mailing.status = 'completed'
            mailing.save()
        return  # Завершаем выполнение функции, так как рассылка завершена

    # Проверяем закончился ли период между рассылками
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

    # Проверяем, готовы ли рассылки к отправке
    if mailing.status in ['created', 'started'] and mailing.start_datetime <= current_datetime:
        try:
            send_mail(
                subject=mailing.message.title,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()] + [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            mailing.status = 'completed'  # Меняем статус на завершено после отправки
            mailing.save()

            MailingLog.objects.create(mailing=mailing, status=True, response='Рассылка успешно отправлена')
            print(f"{mailing} успешно отправлена")

        except smtplib.SMTPException as e:
            MailingLog.objects.create(mailing=mailing, status=False, response=str(e))
            print(f"Ошибка при отправке {mailing}: {e}")


def start_mailing():
    """Функция для начала автоматической рассылки"""
    from main.models import Mailing
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()

    mailings = Mailing.objects.all()

    for mailing in mailings:
        scheduler.add_job(send_mailing, 'interval', seconds=10, args=[mailing])

    scheduler.start()

    while True:
        sleep(1)
