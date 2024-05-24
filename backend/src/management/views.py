import json

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (
    Comment, Dashboard, DashboardProject, Group, Marker,
    Project, ProjectMember, Status, Task, TaskSubscriber,
)
from .permissions import (
    IsCommentCreator, IsCommentManager, IsCommentOwner, IsGroupManager,
    IsInvitationCreator, IsMarkerManager, IsMemberManager, IsProjectManager,
    IsProjectMember, IsProjectOwner, IsStatusManager, IsTaskManager
)
from .serializers import *
from ..notifications.tasks import notify_subscribers
from ..notifications.models import Notification
from ..shared.serializers import EmailSerializer, EmptySerializer
from ..users.permissions import IsAuthenticated


class MapMixin(GenericAPIView):
    action_permissions_map = {}
    action_serializers_map = {}

    def get_serializer_class(self):
        view_action = self.action
        serializer_class = self.action_serializers_map.get(view_action)

        if serializer_class:

            return serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        view_action = self.action
        perm_classes = self.action_permissions_map.get(view_action)
        if perm_classes:
            return [permission() for permission in perm_classes]
        return super().get_permissions()


# class ProjectViewSetMixin(CurrentProfileViewSetMixin, viewsets.GenericViewSet):
#
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['project_pk'] = self.kwargs.get('project_pk')
#         context['instance'] = self.get_queryset().filter(pk=self.kwargs.get('pk')).first()
#         return context


class DashboardViewSet(GenericAPIView):
    queryset = Dashboard.objects
    serializer_class = DashboardDetailSerializer

    def get(self, request, *args, **kwargs):
        dashboard = Dashboard.objects.current(request=request)
        serializer = self.get_serializer(dashboard)
        return Response(data=serializer.data, status=status.HTTP_200_OK, )


class ProjectViewSet(MapMixin, ModelViewSet):
    action_serializers_map = dict(
        list=ProjectListSerializer,
        retrieve=ProjectListSerializer,
        create=ProjectCreateSerializer,
        update=ProjectCreateSerializer,
        partial_update=ProjectCreateSerializer,
        invite=EmailSerializer,
        move=DashboardProjectMoveSerializer
    )

    action_permissions_map = dict(
        list=[IsAuthenticated],
        create=[IsAuthenticated],
        retrieve=[IsAuthenticated, IsProjectMember],
        update=[IsAuthenticated & IsProjectMember & IsProjectManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsProjectManager],
        destroy=[IsAuthenticated & IsProjectOwner],
        invite=[IsAuthenticated & IsProjectMember & IsInvitationCreator],
        move=[IsAuthenticated]
    )

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)

    # def get_object(self):
    #     project = Project.objects.current_or_404(pk=self.kwargs.get('pk'), request=self.request)
    #     self.check_object_permissions(self.request, project)
    #     return project

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)

    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, *args, **kwargs):
        dashboard_project = DashboardProject.objects.current_or_404(
            project_pk=self.kwargs.get('pk'),
            request=self.request,
        )
        serializer = self.get_serializer(instance=dashboard_project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'success': 'Moved'}, status=status.HTTP_200_OK, )

    @transaction.atomic
    @action(detail=True, methods=['post', ], url_path='invite')
    def invite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient_email = serializer.validated_data['email']
        project = self.get_object()
        sender_profile = request.user.profile
        response = project.invite(email=recipient_email, sender=sender_profile)
        return response


class ProjectMemberViewSet(MapMixin, UpdateModelMixin, ReadOnlyModelViewSet):
    action_serializers_map = dict(
        list=MemberListSerializer,
        retrieve=MemberDetailSerializer,
        update=MemberUpdateSerializer,
        partial_update=MemberUpdateSerializer,
        current=MemberCurrentSerializer,
        expel=EmailSerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember],
        retrieve=[IsAuthenticated & IsProjectMember],
        update=[IsAuthenticated & IsProjectMember & IsGroupManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsGroupManager],
        expel=[IsAuthenticated & IsMemberManager],
        deactivate=[IsAuthenticated & IsMemberManager],
        current=[IsAuthenticated & IsProjectMember]
    )

    def get_queryset(self):
        project = Project.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        return ProjectMember.objects.filter(project=project)

    def get_object(self):
        member = ProjectMember.objects.current_or_404(
            pk=self.kwargs.get('pk'),
            project_pk=self.kwargs.get('project_pk'),
            request=self.request,
        )
        self.check_object_permissions(self.request, member)
        return member

    @action(detail=False, methods=['get', ], url_path='current', )
    def current(self, request, *args, **kwargs):
        current_member = ProjectMember.objects.current_or_404(
            project_pk=self.kwargs.get('project_pk'),
            request=self.request,
            profile__user=self.request.user
        )
        serializer = self.get_serializer(instance=current_member)
        return Response(data=serializer.data)

    @transaction.atomic
    @action(detail=True, methods=['post', ], url_path='expel', )
    def expel(self, request, *args, **kwargs):
        member: ProjectMember = self.get_object()
        if member.profile == member.project.owner:
            raise PermissionDenied('Нельзя исключить управляющего проектом.')

        member.delete()
        return Response(data={'success': _('Участник успешно исключен из проекта.')})

    @transaction.atomic
    @action(detail=True, methods=['post', ], url_path='deactivate', serializer_class=EmptySerializer)
    def deactivate(self, request, *args, **kwargs):
        member: ProjectMember = self.get_object()
        if member.profile == member.project.owner:
            raise PermissionDenied('Нельзя отключить управляющего проектом.')

        member.deactivated = True
        member.save()
        return Response(data={'success': _('Участник успешно отключен.')})


class StatusViewSet(MapMixin, ModelViewSet):
    action_serializers_map = dict(
        list=StatusListSerializer,
        retrieve=StatusListSerializer,
        create=StatusCreateSerializer,
        update=StatusCreateSerializer,
        partial_update=StatusCreateSerializer,
        move=StatusMoveSerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember],
        retrieve=[IsAuthenticated & IsProjectMember],
        create=[IsAuthenticated & IsProjectMember & IsStatusManager],
        update=[IsAuthenticated & IsProjectMember & IsStatusManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsStatusManager],
        destroy=[IsAuthenticated & IsProjectMember & IsStatusManager],
        move=[IsAuthenticated & IsStatusManager]
    )

    def get_queryset(self):
        project = Project.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        return Status.objects.filter(Q(project=project)).order_by('order')

    def get_object(self):
        status_ = Status.objects.current_or_404(
            pk=self.kwargs.get('pk'),
            project_pk=self.kwargs.get('project_pk'),
            request=self.request
        )
        self.check_object_permissions(self.request, status_)
        return status_

    def perform_create(self, serializer):
        project = Project.objects.current_or_404(
            pk=self.kwargs.get('project_pk'),
            request=self.request,
        )
        category = serializer.validated_data.get('category')
        if category == 'default':
            serializer.save(project=project)
            return

        with transaction.atomic():
            current_status = Status.objects.filter(project=project, category=category).first()
            new_status = serializer.save(project=project)

            if not current_status:
                return

            current_status.category = 'default'
            current_status.save()
            Task.objects.bulk_update_status(current_status=current_status, new_status=new_status)

    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, *args, **kwargs):
        instance: Status = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(data={'success': 'Moved'}, status=status.HTTP_200_OK, )


class MarkerViewSet(MapMixin, ModelViewSet):
    action_serializers_map = dict(
        list=MarkerListSerializer,
        retrieve=MarkerListSerializer,
        create=MarkerCreateSerializer,
        update=MarkerCreateSerializer,
        partial_update=MarkerCreateSerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember],
        retrieve=[IsAuthenticated & IsProjectMember],
        create=[IsAuthenticated & IsProjectMember & IsMarkerManager],
        update=[IsAuthenticated & IsProjectMember & IsMarkerManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsMarkerManager],
        destroy=[IsAuthenticated & IsProjectMember & IsMarkerManager]
    )

    def get_queryset(self):
        project = Project.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        return Marker.objects.filter(project=project).order_by('-created_at')

    def get_object(self):
        marker = Marker.objects.current_or_404(
            pk=self.kwargs.get('pk'),
            project_pk=self.kwargs.get('project_pk'),
            request=self.request
        )
        self.check_object_permissions(self.request, marker)
        return marker

    def perform_create(self, serializer):
        project = Project.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        serializer.save(project=project)


class GroupViewSet(MapMixin, ModelViewSet):
    action_serializers_map = dict(
        list=GroupListSerializer,
        retrieve=GroupDetailSerializer,
        create=GroupCreateSerializer,
        update=GroupCreateSerializer,
        partial_update=GroupCreateSerializer,
        move=GroupMoveSerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember & IsGroupManager],
        retrieve=[IsAuthenticated & IsProjectMember & IsGroupManager],
        create=[IsAuthenticated & IsProjectMember & IsGroupManager],
        update=[IsAuthenticated & IsProjectMember & IsGroupManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsGroupManager],
        destroy=[IsAuthenticated & IsProjectMember & IsGroupManager],
        move=[IsAuthenticated & IsProjectMember & IsGroupManager]
    )

    def get_queryset(self):
        return Group.objects.filter(project__pk=self.kwargs.get('project_pk')).order_by('order')

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        serializer.save(project=project)

    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, *args, **kwargs):
        group: Group = self.get_object()
        current_member: ProjectMember = ProjectMember.objects.current_or_404(
            pk=self.kwargs.get('project_pk'),
            request=self.request
        )
        first_group_order = current_member.groups.values_list('order', flat=True).order_by('order').first()

        if group.order >= first_group_order and current_member.profile != group.project.owner:
            raise PermissionDenied(
                'Группа заблокирована, потому что эта группа выше, чем ваша самая высокая группа или является ею.'
                '\nПожалуйста, обратитесь за помощью к владельцу более высокой группы или к руководителю проекта.'
            )

        serializer = self.get_serializer(instance=group, data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['order'] >= first_group_order and current_member.profile != group.project.owner:
            raise PermissionDenied(
                'Вы не можете переместить группу выше вашей самой высокой группы.'
                '\nПожалуйста, обратитесь за помощью к владельцу более высокой группы или к руководителю проекта.'
            )

        serializer.save()

        if getattr(group, '_prefetched_objects_cache', None):
            group._prefetched_objects_cache = {}

        return Response(data={'success': 'Moved'}, )


class TaskViewSet(MapMixin, ModelViewSet):
    action_serializers_map = dict(
        list=TaskListSerializer,
        retrieve=TaskDetailSerializer,
        create=TaskCreateSerializer,
        update=TaskCreateSerializer,
        partial_update=TaskCreateSerializer,
        move=TaskMoveSerializer,
        subscribe=EmptySerializer,
        unsubscribe=EmptySerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember],
        retrieve=[IsAuthenticated & IsProjectMember],
        create=[IsAuthenticated & IsProjectMember & IsTaskManager],
        update=[IsAuthenticated & IsProjectMember & IsTaskManager],
        partial_update=[IsAuthenticated & IsProjectMember & IsTaskManager],
        destroy=[IsAuthenticated & IsProjectMember & IsTaskManager],
        move=[IsAuthenticated & IsProjectMember],
        subscribe=[IsAuthenticated & IsProjectMember],
        unsubscribe=[IsAuthenticated & IsProjectMember],
    )

    def get_queryset(self):
        return Task.objects.filter(project__pk=self.kwargs.get('project_pk')).order_by('order')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_pk'] = self.kwargs.get('project_pk')
        context['instance'] = self.get_queryset().filter(pk=self.kwargs.get('pk')).first()
        return context

    def perform_create(self, serializer):
        project = Project.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        current_member = ProjectMember.objects.current_or_404(
            project_pk=self.kwargs.get('project_pk'),
            request=self.request,
            profile__user=self.request.user
        )
        serializer.save(author=current_member, project=project)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        task_data = TaskNotificationSerializer(instance=instance).data
        actor = ProjectMember.objects.current_or_none(project_pk=self.kwargs.get('project_pk'), request=self.request)
        actor_data = MemberDetailSerializer(instance=actor).data
        data = dict(
            action='task_deleted',
            task=task_data,
            actor=actor_data,
        )
        notify_subscribers.delay(data=data)
        return Response(data={'success': 'Задача успешно удалена.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        response.data = {'success': 'Задача успешно перемещена'}
        return response

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, *args, **kwargs):
        task: Task = self.get_object()
        member = ProjectMember.objects.current_or_404(project_pk=self.kwargs.get('project_pk'), request=self.request)
        subscription, created = TaskSubscriber.objects.get_or_create(task=task, subscriber=member)
        if created:
            return Response(data={'success': 'Вы успешно подписались на обновления задачи.'})
        return Response({'message': 'Вы уже подписаны на обновления этой задачи.'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request, *args, **kwargs):
        task: Task = self.get_object()
        member = ProjectMember.objects.current_or_404(project_pk=self.kwargs.get('project_pk'), request=self.request)
        subscription = TaskSubscriber.objects.filter(task=task, subscriber=member).first()
        if not subscription:
            return Response({'message': 'Вы не подписаны на обновления этой задачи.'}, status.HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response({'success': 'Вы успешно отписались от обновлений этой задачи.'})


class CommentViewSet(ModelViewSet):
    action_serializers_map = dict(
        list=CommentListSerializer,
        retrieve=CommentListSerializer,
        create=CommentCreateSerializer,
        update=CommentCreateSerializer,
        partial_update=CommentCreateSerializer,
    )
    action_permissions_map = dict(
        list=[IsAuthenticated & IsProjectMember],
        retrieve=[IsAuthenticated & IsProjectMember],
        create=[IsAuthenticated & IsProjectMember & IsCommentCreator],
        update=[IsAuthenticated & IsProjectMember & IsCommentOwner],
        partial_update=[IsAuthenticated & IsProjectMember & IsCommentOwner],
        destroy=[IsAuthenticated & IsProjectMember & (IsCommentOwner | IsCommentManager)]
    )

    def get_queryset(self):
        task = Task.objects.current_or_404(
            pk=self.kwargs.get('task_pk'),
            project_pk=self.kwargs.get('project_pk'),
            request=self.request
        )
        return Comment.objects.filter(task=task, )

    def get_object(self):
        comment = Comment.objects.current_or_404(
            pk=self.kwargs.get('pk'),
            project_pk=self.kwargs.get('project_pk'),
            task_pk=self.kwargs.get('task_pk'),
            request=self.request
        )
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_create(self, serializer):
        task = Task.objects.current_or_404(pk=self.kwargs.get('project_pk'), request=self.request)
        current_member = ProjectMember.objects.current_or_404(
            project_pk=self.kwargs.get('project_pk'),
            request=self.request,
            profile__user=self.request.user,
        )
        serializer.save(owner=current_member, task=task)
