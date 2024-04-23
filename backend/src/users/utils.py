from datetime import timedelta
from django.conf import settings
from celery.result import AsyncResult
from .tasks import delete_account_task


def get_user_deletion_task_id(user):
    return f'delete_account_{user.delete_id}'


def create_account_deletion_request(user):
    delete_account_task.apply_async(
        kwargs={'user_id': user.id},
        eta=user.deleted_at + timedelta(days=int(settings.USER_ACCOUNT_RESTORE_DAYS)),
        task_id=get_user_deletion_task_id(user),
    )


def safe_revoke(user) -> bool:
    task_id = get_user_deletion_task_id(user)
    result = AsyncResult(task_id)

    if result.status in ('PENDING', 'RECEIVED',):
        result.revoke(terminate=True)
        return True

    return False
