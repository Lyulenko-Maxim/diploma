from django.db import models
from django.utils.translation import gettext_lazy as _

from ..shared.constants import Color
from ..shared.models import UUIDModel


class Permission(UUIDModel):
    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        unique_together = ('name', 'code',)

    name = models.CharField(_('name'), max_length=255, unique=True, )
    code = models.CharField(_('code'), max_length=255, unique=True, )

    def __str__(self):
        return self.name


class Group(UUIDModel):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    name = models.CharField(_('name'), max_length=255, unique=True, )
    color_hex = models.CharField(_('color HEX'), max_length=7, default=Color.WHITE_HEX, )
    position = models.PositiveIntegerField(_('position'), default=0)
    permissions = models.ManyToManyField(Permission, through='GroupPermission', verbose_name='permissions', )
    workspace = models.ForeignKey('management.Workspace', on_delete=models.CASCADE, related_name='groups',
                                  verbose_name=_('workspace'), )


class GroupPermission(UUIDModel):
    class Meta:
        verbose_name = _('group permission')
        verbose_name_plural = _('groups permissions')
        unique_together = ('group', 'permission',)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name=_('permission'))
