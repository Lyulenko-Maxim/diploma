import re

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.shared.models import BaseModel
from .managers import CommentManager, DashboardManager, DashboardProjectManager, GroupManager, MarkerManager, \
    ProjectManager, ProjectMemberManager, StatusManager, TaskManager
from .mixins import OrderableMixin
from ..shared.constants import Color
from ..users.models import Profile

User = get_user_model()

def project_photo_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'projects/{instance.id}/photo.{extension}'

class Project(BaseModel):
    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    objects = ProjectManager()

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True, )
    photo = models.ImageField(
        _('photo'),
        upload_to=project_photo_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='own_projects',
        verbose_name=_('owner'),
    )
    members = models.ManyToManyField(
        to=Profile,
        through='ProjectMember',
        verbose_name=_('members'),
    )

    def save(self, *args, **kwargs):
        if not self._state.adding:
            return super().save(*args, **kwargs)

        with transaction.atomic():
            self._initialize_project()
            return super().save(*args, **kwargs)

    def _initialize_project(self):
        admin = Group.objects.create(project=self, name='Администратор', order=0, color_hex='#FF0000', )
        admin.permissions.set(Permission.objects.all())
        member = Group.objects.create(
            project=self,
            name='Участник',
            order=1,
            color_hex='#1AA744',
            is_default=True,
        )

        owner = ProjectMember.objects.create(project=self, profile=self.owner)
        owner.groups.set([admin])

        Status.objects.create(project=self, name='Сделать', category='todo', order=0, )
        Status.objects.create(project=self, name='В процессе', category='default', order=1, )
        Status.objects.create(project=self, name='Выполнено', category='completed', order=2, )

    def invite(self, email: str, sender: Profile) -> Response:
        from ..notifications.models import Invitation
        recipient: User = User.objects.filter(email=email).first()

        if not recipient:
            return Response(
                data={'error': _('User with this email address was not found')},
                status=status.HTTP_404_NOT_FOUND
            )

        recipient_profile: Profile = recipient.profile

        if Invitation.objects.filter(project=self, recipient=recipient_profile).exists():
            return Response(
                data={'error': _('Данный пользователь уже приглашен в текущий проект.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ProjectMember.objects.filter(project=self, profile=recipient_profile).exists():
            return Response(
                data={'error': _('Данный пользователь уже является участником текущего проекта.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        Invitation.objects.create(project=self, sender=sender, recipient=recipient_profile)

        return Response(data={'success': _('Successfully invited')}, status=status.HTTP_200_OK)


class Dashboard(BaseModel):
    class Meta:
        verbose_name = _('dashboard')
        verbose_name_plural = _('dashboards')

    objects = DashboardManager()

    owner = models.OneToOneField(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='dashboard',
        verbose_name=_('dashboard'),
    )
    projects = models.ManyToManyField(
        to=Project,
        through='DashboardProject',
        blank=True,
        verbose_name=_('projects')
    )


class DashboardProject(OrderableMixin, BaseModel):
    class Meta:
        verbose_name = _('dashboard project')
        verbose_name_plural = _('dashboard projects')
        unique_together = ('dashboard', 'project',)
        ordering = ('order',)

    objects = DashboardProjectManager()

    dashboard = models.ForeignKey(
        to=Dashboard,
        on_delete=models.CASCADE,
        verbose_name=_('dashboard'),
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='dashboards',
        verbose_name=_('project'),
    )

    def get_order_filter_fields(self):
        return {
            'dashboard': self.dashboard,
        }


class Permission(OrderableMixin, BaseModel):
    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ('order',)

    name = models.CharField(_('name'), max_length=255, unique=True, )
    code = models.CharField(_('code'), max_length=255, unique=True, )
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name


class Group(OrderableMixin, BaseModel):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    objects = GroupManager()

    name = models.CharField(_('name'), max_length=255, )
    color_hex = models.CharField(_('color HEX'), max_length=7, default=Color.WHITE_HEX, )
    is_default = models.BooleanField(_('is default'), default=False, )
    permissions = models.ManyToManyField(
        to=Permission,
        through='GroupPermission',
        verbose_name='permissions',
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name=_('project'),
    )

    def __str__(self):
        return f'{self.name}'

    def get_order_filter_fields(self):
        return {'project': self.project, }


class GroupPermission(BaseModel):
    class Meta:
        verbose_name = _('group permission')
        verbose_name_plural = _('groups permissions')
        unique_together = ('group', 'permission',)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name=_('permission'))


class ProjectMember(BaseModel):
    class Meta:
        verbose_name = _('project member')
        verbose_name_plural = _('project members')
        unique_together = ('project', 'profile',)

    objects = ProjectMemberManager()

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='members_set',
        verbose_name=_('project')
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='projects_memberships',
        verbose_name=_('profile')
    )
    groups = models.ManyToManyField(
        to=Group,
        through='ProjectMemberGroup',
        related_name='members',
        verbose_name=_('groups'),
    )
    deactivated = models.BooleanField(_('deactivated'), default=False, )

    @property
    def permissions(self):
        permissions = set()
        groups = self.groups.prefetch_related('permissions').all()
        for group in groups:
            permissions.update(group.permissions.values_list('code', flat=True))
        return permissions

    @property
    def highest_group(self):
        return self.groups.all().order_by('order').first()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            return super().save(*args, **kwargs)

        with transaction.atomic():
            DashboardProject.objects.create(dashboard=self.profile.dashboard, project=self.project)
            default_group = Group.objects.filter(project=self.project, is_default=True).first()
            if not default_group:
                raise ValidationError({'error': _('Assign the default group')})
            self.groups.set([default_group])
            return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.profile.username}'


class ProjectMemberGroup(BaseModel):
    class Meta:
        verbose_name = _('project member group')
        verbose_name_plural = _('project member groups')
        unique_together = ('group', 'member',)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, verbose_name=_('member'))


class Marker(BaseModel):
    class Meta:
        verbose_name = _('marker')
        verbose_name_plural = _('markers')
        ordering = ('created_at',)

    objects = MarkerManager()

    name = models.CharField(_('name'), max_length=255, )
    color_hex = models.CharField(max_length=7, default='#FFFFFF', )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='markers',
        verbose_name=_('project'),
    )

    def __str__(self):
        return f'{self.name}'

    def get_order_filter_fields(self):
        return {'project': self.project, }


class Status(OrderableMixin, BaseModel):
    CATEGORY_CHOICES = [
        ('todo', 'To Do'),
        ('completed', 'Completed'),
        ('default', 'Default'),
    ]

    objects = StatusManager()

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')
        unique_together = ('name', 'project',)

    name = models.CharField(_('name'), max_length=255)
    category = models.CharField(_('category'), max_length=10, choices=CATEGORY_CHOICES, default='default', )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='statuses',
        verbose_name=_('project'),
    )

    def __str__(self):
        return f'{self.name} - {self.get_category_display()}'

    def get_order_filter_fields(self):
        return {'project': self.project, }


class Task(OrderableMixin, BaseModel):
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('highest', 'Highest'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('lowest', 'Lowest'),
    ]

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    objects = TaskManager()

    title = models.CharField(_('title'), max_length=255, )
    description = models.TextField(_('description'), null=True, blank=True, )
    priority = models.CharField(_('priority'), max_length=10, choices=PRIORITY_CHOICES, default='medium', )
    duration = models.PositiveIntegerField(_('duration'), null=True, blank=True, )
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    is_archived = models.BooleanField(_('is archived'), default=False, )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('project'),
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('status'),
    )
    author = models.ForeignKey(
        to=ProjectMember,
        on_delete=models.CASCADE,
        related_name='authored_tasks',
        verbose_name=_('author'),
    )
    assignee = models.ForeignKey(
        to=ProjectMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='assigned_tasks',
        verbose_name=_('assignee'),
    )
    markers = models.ManyToManyField(
        to=Marker,
        through='TaskMarker',
        blank=True,
        default=[],
        verbose_name=_('markers'),
    )
    # parent = models.ForeignKey(
    #     to='self',
    #     on_delete=models.CASCADE,
    #     related_name='subtasks',
    #     null=True,
    #     blank=True,
    #     default=None,
    # )
    dependencies = models.ManyToManyField(
        to='self',
        symmetrical=False,
        through='TaskDependency',
        blank=True,
        default=[],
        verbose_name=_('dependencies'),
    )
    subscribers = models.ManyToManyField(
        to=ProjectMember,
        through='TaskSubscriber',
        related_name='subscriptions',
        blank=True,
        verbose_name=_('subscribers'),
    )

    @property
    def valid_dependencies(self):
        visited = self.dfs()
        return Task.objects.filter(project=self.project).exclude(Q(pk__in=[task.pk for task in visited])).distinct()

    @property
    def available_dependencies(self):
        return self.valid_dependencies.exclude(Q(pk__in=[task.pk for task in self.dependencies.all()])).distinct()

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            #
            # if not self.parent or self.parent in self.dependencies.all():
            #     return super().save(*args, **kwargs)
            #
            # if self._is_cyclic_dependency(self.parent):
            #     raise ValidationError('Задачи не должны образовывать циклическую зависимость.')
            #
            # TaskDependency.objects.create(from_task=self.parent, to_task=self)
            return super().save(*args, **kwargs)

    def _is_cyclic_dependency(self, new_task):
        visited = set()
        dependencies_stack = [self]
        while dependencies_stack:
            task = dependencies_stack.pop()
            if task in visited:
                continue

            visited.add(task)
            if task == new_task:
                return True

            dependencies_stack.extend(task.dependencies.all())
        return False

    def dfs(self, visited=None):
        if visited is None:
            visited = set()

        if self in visited:
            return visited

        visited.add(self)

        dependent_tasks = Task.objects.filter(dependencies=self)

        for dependent_task in dependent_tasks:
            dependent_task.dfs(visited=visited)

        return visited

    def get_order_filter_fields(self):
        return {
            'project': self.project,
            'status': self.status,
        }


class TaskSubscriber(BaseModel):
    class Meta:
        verbose_name = _('task subscriber')
        verbose_name_plural = _('tasks subscribers')
        unique_together = ('task', 'subscriber')

    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        verbose_name=_('subscribers'),
    )
    subscriber = models.ForeignKey(
        to=ProjectMember,
        on_delete=models.CASCADE,
        verbose_name=_('subscriber'),
    )


class TaskDependency(BaseModel):
    class Meta:
        verbose_name = _('task dependency')
        verbose_name_plural = _('tasks dependencies')
        unique_together = ('from_task', 'to_task')

    from_task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='deps',
        verbose_name=_('from task'),
    )
    to_task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='dependent_tasks',
        verbose_name=_('to task'),
    )


class TaskMarker(BaseModel):
    class Meta:
        verbose_name = _('task marker')
        verbose_name_plural = _('tasks markers')
        unique_together = ('task', 'marker',)
        ordering = ('-created_at',)

    marker = models.ForeignKey(
        to=Marker,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('marker'),
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        verbose_name=_('task'),
    )


class Comment(BaseModel):
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-created_at',)

    objects = CommentManager()
    content = models.TextField(_('content'), )
    owner = models.ForeignKey(
        to=ProjectMember,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name=_('owner'),
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('task'),
    )

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.last_edit = timezone.now()
        super().save(*args, **kwargs)

    @property
    def mentioned_members(self):
        pattern = r'@(\w+@\w+\.\w+)'
        matches = re.findall(pattern, self.content)
        return ProjectMember.objects.filter(
            project=self.task.project,
            profile__user__email__in=matches
        )

    # class LogEntry(UUIDModel):
    #     ADDITION = 1
    #     CHANGE = 2
    #     DELETION = 3
    #
    #     ACTION_FLAG_CHOICES = [
    #         (ADDITION, _("Addition")),
    #         (CHANGE, _("Change")),
    #         (DELETION, _("Deletion")),
    #     ]
    #
    #     class Meta:
    #         verbose_name = _('log entry')
    #         verbose_name_plural = _('log entries')
    #         ordering = ["-action_time"]
    #
    #     actor = models.ForeignKey('WorkspaceMember', on_delete=models.CASCADE, verbose_name='logs', )
    #     action_time = models.DateTimeField(_("action time"), default=timezone.now, editable=False, )
    #     content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True,
    #                                      verbose_name=_("content type"), )
    #     object_id = models.UUIDField(_("object id"), blank=True, null=True)
    #     content_object = GenericForeignKey("content_type", "object_id")
    #     action_flag = models.PositiveSmallIntegerField(
    #         _("action flag"), choices=ACTION_FLAG_CHOICES
    #     )
    #     change_message = models.TextField(_("change message"), blank=True)

    # class List(UUIDModel):
    #     class Meta:
    #         verbose_name = _('list')
    #         verbose_name_plural = _('lists')
    #
    #     name = models.CharField(_('name'), max_length=255)
    #     board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists', verbose_name=_('board'), )
    #     order = models.PositiveIntegerField(_('order'), default=0, )
    # class Workspace(UUIDModel):
    #     class Meta:
    #         verbose_name = _('workspace')
    #         verbose_name_plural = _('workspaces')
    #
    #     name = models.CharField(_('name'), max_length=255)
    #     description = models.TextField(_('description'), null=True, blank=True, )
    #     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_workspaces',
    #                               verbose_name=_('owner'), )
    #     members = models.ManyToManyField(Profile, through='WorkspaceMember', verbose_name=_('members'), )

    # class WorkspaceMember(UUIDModel):
    #     class Meta:
    #         verbose_name = _('workspace member')
    #         verbose_name_plural = _('workspaces members')
    #
    #     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, verbose_name=_('board'))
    #     member = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('member'))
    #     date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False, )
    #     groups = models.ManyToManyField(Group, through='WorkspaceMemberGroup', related_name='members',
    #                                     verbose_name=_('groups'), )
    #     deactivated = models.BooleanField(_('deactivated'), default=False, )
    #
    #     def get_permissions(self):
    #         permissions = set()
    #         groups = self.groups.prefetch_related('permissions').all()
    #         for group in groups:
    #             permissions.update(group.permissions.all())
    #         return permissions
    #
    #
    # class WorkspaceMemberGroup(UUIDModel):
    #     class Meta:
    #         verbose_name = _('workspace member group')
    #         verbose_name_plural = _('workspace members groups')
    #         unique_together = ('group', 'member',)
    #
    #     group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    #     member = models.ForeignKey(WorkspaceMember, on_delete=models.CASCADE, verbose_name=_('member'))

    # class Board(UUIDModel, BoardMixin):
    #     class Meta:
    #         verbose_name = _('board')
    #         verbose_name_plural = _('boards')
    #
    #     name = models.CharField(_('name'), max_length=255)
    #     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, verbose_name=_('workspace'))
    #     description = models.TextField(_('description'), null=True, blank=True, )
    #     privacy = models.CharField(_('privacy'), choices=PrivacyType.CHOICES, default=PrivacyType.PRIVATE, max_length=10, )
    #     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_boards', verbose_name=_('owner'), )
    #     members = models.ManyToManyField(Profile, through='BoardMember', verbose_name=_('member'), )
    #     background = models.ForeignKey('BoardBackground', on_delete=models.CASCADE, blank=True, null=True,
    #                                    verbose_name=_('background'), )
    #
    #

    # class TaskExecutor(UUIDModel):
    #     class Meta:
    #         verbose_name = _('task executor')
    #         verbose_name_plural = _('tasks executors')
    #         unique_together = ('task', 'executor',)
    #
    #     executor = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name=_('executor'), )
    #     task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('task'), )
    #     added_at = models.DateTimeField(auto_now_add=True, editable=False, )
    # class BoardMember(UUIDModel):
    #     class Meta:
    #         verbose_name = _('board member')
    #         verbose_name_plural = _('boards members')
    #
    #     board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name=_('board'))
    #     member = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('member'))
    #     date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False, )
    #     deactivated = models.BooleanField(_('deactivated'), default=False, )

    #
    # class CheckList(UUIDModel):
    #     class Meta:
    #         verbose_name = _('check list')
    #         verbose_name_plural = _('checks lists')
    #
    #     name = models.CharField(_('name'), max_length=255)
    #     task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='task', )
    #
    #
    # class Check(UUIDModel):
    #     class Meta:
    #         verbose_name = _('check')
    #         verbose_name_plural = _('checks')
    #
    #     title = models.CharField(_('title'), max_length=255, )
    #     deadline = models.DateTimeField(_('deadline'), null=True, blank=True, )
    #     is_completed = models.BooleanField(_('is completed'), default=False, )
    #     check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, verbose_name=_('check list'), )
    #     executors = models.ManyToManyField(BoardMember, through='CheckExecutor', verbose_name=_('executors'), )
    #
    #
    # class CheckExecutor(UUIDModel):
    #     class Meta:
    #         verbose_name = _('check executor')
    #         verbose_name_plural = _('checks executors')
    #         unique_together = ('check_box', 'executor')
    #
    #     executor = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name=_('executor'), )
    #     check_box = models.ForeignKey(Check, on_delete=models.CASCADE, verbose_name=_('check'), )
    #     added_at = models.DateTimeField(auto_now_add=True, editable=False, )

    # class BoardBackground(UUIDModel):
    #     class Meta:
    #         verbose_name = _('board background')
    #         verbose_name_plural = _('boards backgrounds')
    #
    #     image = models.ImageField(upload_to='', null=True, blank=True, )
    #     color_hex = models.CharField(max_length=7, null=True, blank=True, )
    #     is_public = models.BooleanField(_('is public'), default=False, )

    # class Attachment(UUIDModel):
    #     class Meta:
    #         verbose_name = _('attachment')
    #         verbose_name_plural = _('attachments')
    #
    #     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attachments', verbose_name=_('owner'), )
    #     content = models.FileField(upload_to='', )
    #     is_cover = models.BooleanField(_('is cover'), default=False, )

    #
    # class BoardTemplate(UUIDModel):
    #     class Meta:
    #         verbose_name = _('board template')
    #         verbose_name_plural = _('boards templates')
    #
    #     board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name=_('board'), )
    #     is_public = models.BooleanField(_('is_public'), default=False, )

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
