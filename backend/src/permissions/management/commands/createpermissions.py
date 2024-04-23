from django.core.management.base import BaseCommand
from django.db import transaction
from src.shared.constants import Permissions
from ...models import Permission


class Command(BaseCommand):
    help = 'Creates permissions if they do not exist'

    def handle(self, *args, **options):
        with transaction.atomic():
            for name, code in Permissions.DATA:
                perm, created = Permission.objects.get_or_create(name=name, code=code)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Permission "{name}" created'))
                else:
                    self.stdout.write(self.style.WARNING(f'Permission "{name}" already exists'))
