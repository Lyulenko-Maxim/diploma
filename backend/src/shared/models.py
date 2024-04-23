import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, unique=True, editable=False, )
