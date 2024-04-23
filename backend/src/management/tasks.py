# from django.utils import timezone
#
# from core.celery import app
# from .models import Task
# from telegram import Bot
#
#
# @app.task
# def send_telegram_notification(chat_id, message):
#     bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
#     bot.send_message(chat_id=chat_id, text=message)
#
#
# @app.task
# def update_tasks_overdue_status():
#     overdue_tasks = Task.objects.filter(
#         deadline__lt=timezone.now(),
#         status__in=['pending', 'in_progress'],
#     )
#     overdue_tasks.update(is_overdue=True, )
#
#

from celery import shared_task
from django.contrib.auth import get_user_model
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
#
# from src.authentication.helpers import generate_activation_link, get_current_host
#
# User = get_user_model()
#
#
# @shared_task()
# def send_activation_link(user_id):
#     print(get_current_host())
#     try:
#         user = User.objects.get(pk=str(user_id))
#         activation_link = generate_activation_link(user)
#         data = {
#             'email': user.email,
#             'content_message': 'We are happy that we defined communicate with as!',
#             'activation_link': f'{get_current_host()}/api/authentication/activate/{activation_link}/'
#         }
#         message_html = render_to_string('activation_email.html', data)
#         message = strip_tags(message_html)
#         email = EmailMultiAlternatives(
#             subject='Activation email',
#             body=message,
#             from_email='taskmanagementby@mail.com',
#             to=[user.email],
#         )
#         email.attach_alternative(message_html, 'text/html')
#         email.send()
#     except User.DoesNotExist:
#         pass
