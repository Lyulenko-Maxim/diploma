from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.shared.models import UUIDModel
from src.shared.models import UUIDModel
from src.users.models import Profile
from .mixins import InvitationMixin
from ..management.models import Board, Workspace
from ..shared.constants import InvitationType

User = get_user_model()


class Notification(UUIDModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('profile'), )
    message = models.TextField(_('message'), )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)


class Invitation(UUIDModel, InvitationMixin):
    # type = models.CharField(_('type'), max_length=10, choices=InvitationType.CHOICES,
    #                         default=InvitationType.WORKSPACE, )
    # board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='invitations',
    #                           null=True, blank=True, verbose_name='board', )
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='invitations',
                                  null=True, blank=True, verbose_name='workspace', )
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='invitations_sent',
                               verbose_name='sender', )
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='invitations_got',
                                  verbose_name='recipient', )
    invited_at = models.DateTimeField(_('date joined'), auto_now_add=True, editable=False, )

    # def save(self, *args, **kwargs):
    #     if self.type == InvitationType.BOARD:
    #         self.team = None
    #
    #     elif self.type == InvitationType.WORKSPACE:
    #         self.board = None
    #
    #     super().save(*args, **kwargs)
