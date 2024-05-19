from django.core.management.base import BaseCommand
from django.db import transaction
from ...models import Permission
from ...permissions import PERMISSIONS_DATA


class Command(BaseCommand):
    help = 'Creates permissions if they do not exist'

    @transaction.atomic
    def handle(self, *args, **options):
        for name, description, code, order in PERMISSIONS_DATA:
            perm, created = Permission.objects.update_or_create(
                code=code,
                defaults=dict(
                    name=name,
                    description=description,
                    order=order
                )
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission "{name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Permission "{name}" updated'))
