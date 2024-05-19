import json
import logging

from celery import shared_task
from firebase_admin import messaging
from push_notifications.models import GCMDevice

from src.notifications.models import Notification
from src.users.models import Profile

logger = logging.getLogger(__name__)


def convert_to_str(data):
    if isinstance(data, dict):
        return {str(key): str(json.dumps(value)) for key, value in data.items()}


@shared_task
def notify_expelled_member(data):
    Notification.objects.create(action='expelled', data=data, recipient=data['member']['profile'])
    title = f"Вы были исключены из прокта {data['project']['name']}"
    profile = data.pop('member')
    device = GCMDevice.objects.filter(user__profile=profile, active=True).first()

    if not device:
        return

    device.send_message(messaging.Message(
        data=data,
        notification=messaging.Notification(title=title),
    ))


@shared_task
def notify_subscribers(data):
    subscribers = data['task'].pop('subscribers')
    action = data['action']

    recipients = Profile.objects.filter(user__id__in=subscribers)

    for recipient in recipients:
        Notification.objects.create(action=action, data=data, recipient=recipient)

    task_title = data['task']['title']

    if action == 'task_updated':
        title = f"Задача {task_title} была обновлена"

    elif action == 'task_deleted':
        title = f"Задача {task_title} была удалена"

    elif action == 'task_moved':
        title = f"Задача {task_title} была перемещена"

    else:
        title = "Уведомление о задаче"

    devices = GCMDevice.objects.filter(user__in=subscribers, active=True)

    if not devices:
        return

    str_data = convert_to_str(data)
    devices.send_message(messaging.Message(
        data=str_data,
        notification=messaging.Notification(title=title),
    ))
