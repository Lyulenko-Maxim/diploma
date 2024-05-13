from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..shared.serializers import EmailSerializer, EmptySerializer
from ..users.models import Profile
from . import permissions
from .models import (
    Comment,
    Dashboard,
    DashboardProject,
    Group,
    Marker,
    Project,
    ProjectMember,
    Status,
    Task,
)
from .serializers import (
    CommentSerializer,
    DashboardProjectSerializer,
    DashboardSerializer,
    GroupListSerializer, GroupSerializer,
    MarkerSerializer,
    ProjectListSerializer, ProjectMemberAssignSerializer, ProjectMemberListSerializer, ProjectMemberSerializer,
    ProjectSerializer,
    RTaskSerializer,
    StatusSerializer,
)


class DashboardViewSetMixin(viewsets.GenericViewSet):
    def get_current_profile(self):
        profile: Profile = self.request.user.profile
        return profile


class ProjectViewSetMixin(viewsets.GenericViewSet):
    def get_current_profile(self):
        profile: Profile = self.request.user.profile
        return profile

    def get_current_dashboard(self):
        profile = self.get_current_profile()
        dashboard: Dashboard = get_object_or_404(Dashboard, owner=profile)
        return dashboard

    def get_current_project_or_404(self):
        dashboard = self.get_current_dashboard()
        project: Project = get_object_or_404(Project.objects.filter(
            Q(pk=self.kwargs.get('project_pk'))
            & (Q(dashboards__dashboard=dashboard))
        ).distinct())
        return project

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['project_pk'] = self.kwargs.get('project_pk')
        context['instance'] = self.get_queryset().filter(pk=self.kwargs.get('pk')).first()
        return context


class DashboardViewSet(DashboardViewSetMixin):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects

    def get_serializer_class(self):
        if self.action == 'move':
            self.serializer_class = DashboardProjectSerializer
        else:
            self.serializer_class = DashboardSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request, *args, **kwargs):
        profile = self.get_current_profile()
        dashboard: Dashboard = get_object_or_404(Dashboard, owner=profile)
        serializer = self.get_serializer(dashboard)
        return Response(data=serializer.data, status=status.HTTP_200_OK, )


class ProjectViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        dashboard = self.get_current_dashboard()
        return Project.objects.filter(dashboards__dashboard=dashboard).distinct()

    def get_serializer_class(self):
        if self.action in ('list',):
            self.serializer_class = ProjectListSerializer
        elif self.action in ('invite',):
            self.serializer_class = EmailSerializer
        elif self.action in ('move',):
            self.serializer_class = DashboardProjectSerializer
        else:
            self.serializer_class = ProjectSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateProject]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteProject]
        elif self.action in ('invite',):
            self.permission_classes = [IsAuthenticated, permissions.CanInviteMember]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        with transaction.atomic():
            profile = self.get_current_profile()
            serializer.save(owner=profile)

    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, *args, **kwargs):
        profile = self.get_current_profile()
        project: Project = self.get_object()
        dashboard: Dashboard = get_object_or_404(Dashboard, owner=profile)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dp = get_object_or_404(DashboardProject, project=project, dashboard=dashboard)
        dp.order = serializer.validated_data['order']
        dp.save()
        return Response(data={'success': 'Moved'}, status=status.HTTP_200_OK, )

    @action(detail=True, methods=['post', ], url_path='invite')
    def invite(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            recipient_email = serializer.validated_data['email']
            project: Project = self.get_object()
            sender_profile: Profile = request.user.profile
            response = project.invite(email=recipient_email, sender=sender_profile)
            return response


class ProjectMemberViewSet(ProjectViewSetMixin, mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        project = self.get_current_project_or_404()
        return ProjectMember.objects.filter(Q(project=project))

    def get_serializer_class(self):
        if self.action in ('list',):
            self.serializer_class = ProjectMemberListSerializer
        elif self.action in ('update', 'partial_update',):
            self.serializer_class = ProjectMemberAssignSerializer
        else:
            self.serializer_class = ProjectMemberSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('expel',):
            self.permission_classes = [IsAuthenticated, permissions.CanExpelMember]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanAssignGroup]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=True, methods=['post', ], url_path='expel', serializer_class=EmptySerializer)
    def expel(self, request, *args, **kwargs):
        with transaction.atomic():
            member: ProjectMember = self.get_object()

            if member.profile == member.project.owner:
                return Response(data={'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

            member.delete()
            return Response(data={'success': _('Successfully expelled')}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', ], url_path='deactivate', serializer_class=EmptySerializer)
    def deactivate(self, request, *args, **kwargs):
        with transaction.atomic():
            member: ProjectMember = self.get_object()

            if member.profile == member.project.owner:
                return Response(data={'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

            member.deactivated = True
            member.save()
            return Response(data={'success': _('Successfully deactivated')}, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['put', ], url_path='assign-group', serializer_class=ProjectMemberSerializer)
    # def assign_group(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         member: ProjectMember = self.get_object()
    #
    #         if member.profile == member.project.owner:
    #             return Response(data={'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)
    #
    #         member.deactivated = True
    #         member.save()
    #         return Response(data={'success': _('Successfully deactivated')}, status=status.HTTP_200_OK)


class StatusViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.filter(Q(project=self.get_current_project_or_404())).order_by('order')

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, permissions.CanCreateStatus]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateStatus]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteStatus]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = self.get_current_project_or_404()
        data = serializer.validated_data
        category = data.get('category')

        if not category == 'default':
            current_status = Status.objects.filter(project=project, category=category).first()
            status_ = serializer.save(project=project)
            with transaction.atomic():
                if not current_status:
                    return

                current_status.category = 'default'
                current_status.save()
                Task.bulk_update_status(current_status=current_status, new_status=status_)
                return

        serializer.save(project=project)


class MarkerViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = MarkerSerializer

    def get_queryset(self):
        project = self.get_current_project_or_404()
        return Marker.objects.filter(Q(project=project)).order_by('order')

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, permissions.CanCreateMarker]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateMarker]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteMarker]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = self.get_current_project_or_404()
        serializer.save(project=project)


class GroupViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        project = self.get_current_project_or_404()
        return Group.objects.filter(Q(project=project)).order_by('order')

    def get_serializer_class(self):
        if self.action in ('list',):
            self.serializer_class = GroupListSerializer
        else:
            self.serializer_class = GroupSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('retrieve', 'list',):
            self.permission_classes = [IsAuthenticated, permissions.CanViewGroup]
        elif self.action in ('create',):
            self.permission_classes = [IsAuthenticated, permissions.CanCreateGroup]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateGroup]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteGroup]
        elif self.action in ('assign',):
            self.permission_classes = [IsAuthenticated, permissions.CanAssignGroup]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = self.get_current_project_or_404()
        serializer.save(project=project)


class TaskViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = RTaskSerializer

    def get_queryset(self):
        project = self.get_current_project_or_404()
        return Task.objects.filter(Q(project=project))

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, permissions.CanCreateTask]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateTask]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteTask]
        elif self.action in ('assign',):
            self.permission_classes = [IsAuthenticated, permissions.CanAssignTask]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        profile = self.get_current_profile()
        project = self.get_current_project_or_404()
        member = get_object_or_404(ProjectMember, project=project, profile=profile)
        serializer.save(author=member, project=project)


class CommentViewSet(ProjectViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        project = self.get_current_project_or_404()
        task = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), project=project)
        return Comment.objects.filter(Q(task=task))

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, permissions.CanCreateComment]
        elif self.action in ('update', 'partial_update',):
            self.permission_classes = [IsAuthenticated, permissions.CanUpdateComment]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, permissions.CanDeleteComment]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        profile = self.get_current_profile()
        project = self.get_current_project_or_404()
        member = get_object_or_404(ProjectMember, project=project, profile=profile)
        task = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), project=project)
        serializer.save(owner=member, task=task)
