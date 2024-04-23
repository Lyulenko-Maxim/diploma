from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@shared_task
def delete_account_task(user_id):
    with transaction.atomic():
        try:
            user = User.objects.get(pk=str(user_id))
            user.delete()
        except User.DoesNotExist:
            pass
