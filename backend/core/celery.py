import os
import time

from celery import Celery
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task
def debug_task():
    time.sleep(20)
    print("debug task working")


@app.task
def send_email(email: str, template_name: str, subject: str, context: dict):
    try:
        message_html = render_to_string(template_name, context)
        message = strip_tags(message_html)
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        email.attach_alternative(message_html, 'text/html')
        email.send()
    except Exception as e:
        print(f'Failed to send email: {e}')
