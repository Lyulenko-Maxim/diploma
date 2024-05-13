from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.shared.models import UUIDModel
from src.shared.models import UUIDModel
from src.users.models import Profile
from .mixins import InvitationMixin
from ..management.models import Project, ProjectMember

User = get_user_model()


class Notification(UUIDModel):
    message = models.TextField(_('message'), )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    recipient = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('recipient'),
    )


class Invitation(UUIDModel, InvitationMixin):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='invitations',
        verbose_name='workspace', )
    sender = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='invitations_sent',
        verbose_name='sender',
    )
    recipient = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='invitations_got',
        verbose_name='recipient',
    )
    invited_at = models.DateTimeField(_('date joined'), default=timezone.now, editable=False, )


class InvitationLink(UUIDModel):
    class Meta:
        verbose_name = _('invitation link')
        verbose_name_plural = _('invitation links')

    creator = models.ForeignKey(
        to=ProjectMember,
        on_delete=models.CASCADE,
        related_name='invitation_links',
        verbose_name=_('creator'),
    )

    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False, )
    expire_at = models.DateTimeField(_('expire at'), blank=True, null=True, )
    uses_count = models.PositiveIntegerField(_('uses count'), default=0, editable=False, )
    max_uses_count = models.PositiveIntegerField(_('max uses count'), blank=True, null=True, )

    def is_active(self):
        return not self._is_expired() and not self._is_uses_exceeded()

    def _is_uses_exceeded(self):
        return self.uses_count >= self.max_uses_count

    def _is_expired(self):
        return self.expire_at and self.expire_at < timezone.now()
