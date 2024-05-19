import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models, transaction
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, unique=True, editable=False, )


class LifeCycleUUIDModel(UUIDModel):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False, )
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now, editable=False, )


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, unique=True, editable=False, )
    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False, )
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now, editable=False, )


class OrderableMixin(models.Model):
    class Meta:
        abstract = True

    order = models.PositiveIntegerField(_('order'), default=0)

    def get_order_filter_fields(self) -> dict:
        return {}

    def _move(self, from_pos, to_pos):
        filters = self.get_order_filter_fields()

        if to_pos > from_pos:
            query = Q(order__gt=from_pos) & Q(order__lte=to_pos)
            offset = -1
        else:
            query = Q(order__lt=from_pos) & Q(order__gte=to_pos)
            offset = 1

        self.__class__.objects \
            .filter(**filters) \
            .filter(query) \
            .exclude(pk=self.pk) \
            .distinct() \
            .update(order=F('order') + offset)

    def update_order_after_delete(self, from_pos):
        self.__class__.objects \
            .filter(**self.get_order_filter_fields()) \
            .filter(order__gt=from_pos) \
            .update(order=F('order') - 1)

    def _update_order_after_insert(self):
        filters = self.get_order_filter_fields()
        count = self.__class__.objects.filter(**filters).count()
        max_order = count if count != 0 else 0
        if self.order > max_order:
            self.order = max_order

        if self.order == max_order:
            return

        self._move(from_pos=max_order, to_pos=self.order)

    def _update_order_after_update(self):
        old_instance = get_object_or_404(self.__class__, pk=self.pk)
        filters = old_instance.get_order_filter_fields()

        if filters != self.get_order_filter_fields():
            old_instance.update_order_after_delete(old_instance.order)
            self._update_order_after_insert()
            return

        from_pos = old_instance.order

        count = self.__class__.objects.filter(**filters).count()
        max_order = count - 1 if count != 0 else 0
        if self.order > max_order:
            self.order = max_order

        if self.order == from_pos:
            return

        self._move(from_pos=from_pos, to_pos=self.order)

    def save(self, *args, **kwargs):
        if self._state.adding:
            with transaction.atomic():
                self._update_order_after_insert()
                return super().save(*args, **kwargs)

        with transaction.atomic():
            self._update_order_after_update()
            return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            from_pos = self.order
            super().delete(*args, **kwargs)
            self.update_order_after_delete(from_pos)
