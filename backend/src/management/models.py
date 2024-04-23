import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..shared.constants import PrivacyType
from ..shared.models import UUIDModel
from ..users.models import Profile
from ..permissions.models import Group, Permission
from .mixins import BoardMixin

User = get_user_model()


class Workspace(UUIDModel):
    class Meta:
        verbose_name = _('workspace')
        verbose_name_plural = _('workspaces')

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True, )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_workspaces',
                              verbose_name=_('owner'), )
    members = models.ManyToManyField(Profile, through='WorkspaceMember', verbose_name=_('members'), )


class WorkspaceMember(UUIDModel):
    class Meta:
        verbose_name = _('workspace member')
        verbose_name_plural = _('workspaces members')

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, verbose_name=_('board'))
    member = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('member'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False, )
    groups = models.ManyToManyField(Group, through='WorkspaceMemberGroup', related_name='members',
                                    verbose_name=_('groups'), )
    deactivated = models.BooleanField(_('deactivated'), default=False, )

    def get_permissions(self):
        permissions = set()
        groups = self.groups.prefetch_related('permissions').all()
        for group in groups:
            permissions.update(group.permissions.all())
        return permissions


class WorkspaceMemberGroup(UUIDModel):
    class Meta:
        verbose_name = _('workspace member group')
        verbose_name_plural = _('workspace members groups')
        unique_together = ('group', 'member',)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    member = models.ForeignKey(WorkspaceMember, on_delete=models.CASCADE, verbose_name=_('member'))


class Board(UUIDModel, BoardMixin):
    class Meta:
        verbose_name = _('board')
        verbose_name_plural = _('boards')

    name = models.CharField(_('name'), max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, verbose_name=_('workspace'))
    description = models.TextField(_('description'), null=True, blank=True, )
    privacy = models.CharField(_('privacy'), choices=PrivacyType.CHOICES, default=PrivacyType.PRIVATE, max_length=10, )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_boards', verbose_name=_('owner'), )
    members = models.ManyToManyField(Profile, through='BoardMember', verbose_name=_('member'), )
    background = models.ForeignKey('BoardBackground', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name=_('background'), )


class BoardMember(UUIDModel):
    class Meta:
        verbose_name = _('board member')
        verbose_name_plural = _('boards members')

    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name=_('board'))
    member = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('member'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False, )
    deactivated = models.BooleanField(_('deactivated'), default=False, )


class Marker(UUIDModel):
    class Meta:
        verbose_name = _('marker')
        verbose_name_plural = _('markers')

    name = models.CharField(_('name'), max_length=255, )
    color_hex = models.CharField(max_length=7, null=True, blank=True, )
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='markers', verbose_name=_('board'), )


class List(UUIDModel):
    class Meta:
        verbose_name = _('list')
        verbose_name_plural = _('lists')

    name = models.CharField(_('name'), max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists', verbose_name=_('board'), )
    order = models.PositiveIntegerField(_('order'), default=0, )


class Task(UUIDModel):
    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    title = models.CharField(_('title'), max_length=255, )
    description = models.TextField(_('description'), null=True, blank=True, )
    list = models.ForeignKey(List, on_delete=models.CASCADE, verbose_name=_('list'), )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_tasks',
                              verbose_name=_('owner'), )
    deadline = models.DateTimeField(_('deadline'), default=None, null=True, blank=True, )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, )
    is_archived = models.BooleanField(_('is archived'), default=False, )
    # viewers = models.ManyToManyField(Profile, through='TaskViewer', verbose_name=_('viewers'), )
    executors = models.ManyToManyField(BoardMember, through='TaskExecutor', verbose_name=_('executors'))
    markers = models.ManyToManyField(Marker, through='TaskMarker', verbose_name=_('markers'))


class TaskMarker(UUIDModel):
    class Meta:
        verbose_name = _('task marker')
        verbose_name_plural = _('tasks markers')
        unique_together = ('task', 'marker',)

    marker = models.ForeignKey(Marker, on_delete=models.CASCADE, verbose_name=_('marker'), )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('task'), )
    added_at = models.DateTimeField(auto_now_add=True, editable=False, )


class TaskExecutor(UUIDModel):
    class Meta:
        verbose_name = _('task executor')
        verbose_name_plural = _('tasks executors')
        unique_together = ('task', 'executor',)

    executor = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name=_('executor'), )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('task'), )
    added_at = models.DateTimeField(auto_now_add=True, editable=False, )


class Comment(UUIDModel):
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    content = models.TextField(_('content'), )
    sender = models.ForeignKey(BoardMember, on_delete=models.SET_NULL, null=True, verbose_name=_('sender'), )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name=_('task'), )

    @property
    def mentioned_board_members(self):
        pattern = r'@(\w+)'
        matches = re.findall(pattern, self.content)
        mentioned_members = BoardMember.objects.filter(member__user__email__in=matches)
        return mentioned_members


class CheckList(UUIDModel):
    class Meta:
        verbose_name = _('check list')
        verbose_name_plural = _('checks lists')

    name = models.CharField(_('name'), max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='task', )


class Check(UUIDModel):
    class Meta:
        verbose_name = _('check')
        verbose_name_plural = _('checks')

    title = models.CharField(_('title'), max_length=255, )
    deadline = models.DateTimeField(_('deadline'), null=True, blank=True, )
    is_completed = models.BooleanField(_('is completed'), default=False, )
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, verbose_name=_('check list'), )
    executors = models.ManyToManyField(BoardMember, through='CheckExecutor', verbose_name=_('executors'), )


class CheckExecutor(UUIDModel):
    class Meta:
        verbose_name = _('check executor')
        verbose_name_plural = _('checks executors')
        unique_together = ('check_box', 'executor',)

    executor = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name=_('executor'), )
    check_box = models.ForeignKey(Check, on_delete=models.CASCADE, verbose_name=_('check'), )
    added_at = models.DateTimeField(auto_now_add=True, editable=False, )


class BoardBackground(UUIDModel):
    class Meta:
        verbose_name = _('board background')
        verbose_name_plural = _('boards backgrounds')

    image = models.ImageField(upload_to='', null=True, blank=True, )
    color_hex = models.CharField(max_length=7, null=True, blank=True, )
    is_public = models.BooleanField(_('is public'), default=False, )


class Attachment(UUIDModel):
    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attachments', verbose_name=_('owner'), )
    content = models.FileField(upload_to='', )
    is_cover = models.BooleanField(_('is cover'), default=False, )


class BoardTemplate(UUIDModel):
    class Meta:
        verbose_name = _('board template')
        verbose_name_plural = _('boards templates')

    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name=_('board'), )
    is_public = models.BooleanField(_('is_public'), default=False, )

# class TaskViewer(UUIDModel):
#     class Meta:
#         verbose_name = _('task viewer')
#         verbose_name_plural = _('management viewers')
#         unique_together = ('viewer', 'task')
#
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_viewers', verbose_name=_('task'), )
#     viewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='viewed_tasks',
#                                verbose_name=_('viewer'), )
#     viewed_at = models.DateTimeField(auto_now_add=True, )
#
#
# class Event(UUIDModel):
#     class Meta:
#         verbose_name = _('event')
#         verbose_name_plural = _('events')
#
#     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='events', verbose_name=_('event owner'), )
#     title = models.CharField(_('event title'), max_length=255, )
#     description = models.TextField(_('event description'), )
#     start_time = models.DateTimeField(_('event start time'), )
#     end_time = models.DateTimeField(_('event end time'), )
#     created = models.DateTimeField(_('created at'), auto_now_add=True, )
#     is_ended = models.BooleanField(_('is ended'), default=False)
