from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Board, BoardMember, CheckList, List, Marker, Task, Workspace, WorkspaceMember
from .permissions import CanEditBoardPermission
from .serializers import (
    BoardMemberReadSerializer,
    BoardReadSerializer,
    BoardSerializer,
    CheckListReadSerializer, CheckListSerializer, ListReadSerializer,
    ListSerializer,
    MarkerReadSerializer, TaskReadSerializer, TaskSerializer, WorkspaceMemberReadSerializer, WorkspaceMemberSerializer,
    WorkspaceReadSerializer,
    WorkspaceSerializer,
)
from ..notifications.models import Invitation
from ..permissions.models import Group
from ..permissions.permissions import HasGroupPermission
from ..permissions.serializers import GroupReadSerializer, GroupSerializer
from ..shared.serializers import EmailSerializer, EmptySerializer
from ..users.models import Profile

User = get_user_model()


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter((Q(owner=profile) | Q(members=profile))).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            self.serializer_class = WorkspaceReadSerializer
        if self.action in ('create', 'update', 'partial_update', 'delete',):
            self.serializer_class = WorkspaceSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        workspace: Workspace = serializer.save()
        WorkspaceMember.objects.get_or_create(workspace=workspace, member=workspace.owner)


class WorkspaceMemberViewSet(NestedViewSetMixin, mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkspaceMemberReadSerializer
    queryset = WorkspaceMember.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(workspace__owner=profile) | Q(workspace__members=profile))
        )
        if not queryset.exists():
            raise Http404("No WorkspaceMember matches the given query.")

        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            self.serializer_class = WorkspaceMemberReadSerializer
        else:
            self.serializer_class = WorkspaceMemberSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['workspace_pk'] = self.kwargs.get('workspace_pk')
        return context

    @action(detail=False, methods=['post', ], url_path='invite', serializer_class=EmailSerializer)
    def invite(self, request, *args, **kwargs):
        with transaction.atomic():
            recipient_email = request.data.get('email')
            workspace_pk = self.kwargs.get('workspace_pk')
            workspace: Workspace = get_object_or_404(Workspace, pk=workspace_pk)
            recipient_user: User = User.objects.filter(email=recipient_email).first()

            if not recipient_user:
                return Response({'error': _('User with this email address was not found')},
                                status=status.HTTP_404_NOT_FOUND)

            recipient_profile: Profile = recipient_user.profile
            sender_profile: Profile = request.user.profile

            if Invitation.objects.filter(workspace=workspace, recipient=recipient_profile).exists():
                return Response({'error': _('This user is already invited to the workspace')},
                                status=status.HTTP_400_BAD_REQUEST)

            if WorkspaceMember.objects.filter(workspace=workspace, member=recipient_profile).exists():
                return Response({'error': _('This user is already a member of the workspace')},
                                status=status.HTTP_400_BAD_REQUEST)

            Invitation.objects.create(workspace=workspace, sender=sender_profile, recipient=recipient_profile)

            return Response({'success': _('Successfully invited')}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', ], url_path='expel', serializer_class=EmptySerializer)
    def expel(self, request, *args, **kwargs):
        with transaction.atomic():
            member = self.get_object()
            workspace = get_object_or_404(Workspace, pk=self.kwargs['workspace_pk'])
            if member == workspace.owner:
                return Response({'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

            member.delete()
            return Response({'success': _('Successfully expelled')}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', ], url_path='deactivate', serializer_class=EmptySerializer)
    def deactivate(self, request, *args, **kwargs):
        with transaction.atomic():
            member = self.get_object()
            workspace = get_object_or_404(Workspace, pk=self.kwargs['workspace_pk'])
            if member == workspace.owner:
                return Response({'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

            member.deactivated = True
            member.save()
            return Response({'success': _('Successfully deactivated')}, status=status.HTTP_200_OK)


class WorkspaceGroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, HasGroupPermission]
    queryset = Group.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(workspace__owner=profile) | Q(workspace__members=profile))
        )
        if not queryset.exists():
            raise Http404("No WorkspaceGroup matches the given query.")

        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            self.serializer_class = GroupReadSerializer
        else:
            self.serializer_class = GroupSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['workspace_pk'] = self.kwargs.get('parent_lookup_workspace')
        return context

    def perform_create(self, serializer):
        workspace = get_object_or_404(
            Workspace,
            Q(pk=self.kwargs['parent_lookup_workspace']) &
            (Q(owner=self.request.user.profile) | Q(members=self.request.user.profile))
        )
        serializer.save(workspace=workspace)


class BoardViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(workspace__owner=profile) | Q(workspace__members=profile))
        )
        if not queryset.exists():
            raise Http404("No Board matches the given query.")

        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.serializer_class = BoardReadSerializer

        if self.action in ('create', 'update', 'partial_update', 'delete'):
            self.serializer_class = BoardSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            self.permission_classes = [permissions.IsAuthenticated, CanEditBoardPermission]

        return super().get_permissions()

    def perform_create(self, serializer):
        workspace = get_object_or_404(
            Workspace,
            Q(pk=self.kwargs['parent_lookup_workspace']) &
            (Q(owner=self.request.user.profile) | Q(members=self.request.user.profile))
        )
        serializer.save(workspace=workspace)

    @action(detail=True, methods=['post', ], url_path='join', serializer_class=EmptySerializer)
    def join(self, request, *args, **kwargs):
        profile: Profile = self.request.user.profile
        board: Board = self.get_object()
        _, created = BoardMember.objects.get_or_create(board=board, member=profile)
        if not created:
            return Response({'error': 'You are already member of this board.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Successfully joined.'}, status=status.HTTP_200_OK)


class BoardMemberViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardMemberReadSerializer
    queryset = BoardMember.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(board__workspace__owner=profile) | Q(board__workspace__members=profile))
            & (Q(board__owner=profile) | Q(board__members=profile))
        )
        if not queryset.exists():
            raise Http404("No BoardMember matches the given query.")

        return queryset

    def get_serializer_class(self):
        return super().get_serializer_class()

    # @action(detail=False, methods=['post', ], url_path='invite', serializer_class=EmailSerializer)
    # def invite(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         recipient_email = self.request.data.get('email')
    #         board = get_object_or_404(Board, pk=self.kwargs['board_pk'])
    #         response = board.invite(sender=self.request.user.profile, email=recipient_email)
    #         return response
    #
    # @action(detail=True, methods=['post', ], url_path='expel', serializer_class=EmptySerializer)
    # def expel(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         member = self.get_object()
    #         board = get_object_or_404(Board, pk=self.kwargs['board_pk'])
    #         response = board.expel(member)
    #         return response
    #
    # @action(detail=True, methods=['put', ], url_path='grant', serializer_class=BoardMemberPermissionSerializer)
    # def grant_permissions(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         member = self.get_object()
    #         serializer = self.get_serializer(instance=member, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response({'success': _('Permissions granted successfully.')}, status=status.HTTP_200_OK)


class MarkerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarkerReadSerializer
    queryset = Marker.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(board__workspace__owner=profile) | Q(board__workspace__members=profile))
            & (Q(board__owner=profile) | Q(board__members=profile))
        )
        # if not queryset.exists():
        #     raise Http404("No BoardMember matches the given query.")

        return queryset

    def get_serializer_class(self):
        return super().get_serializer_class()

    def perform_create(self, serializer):
        board_pk = self.kwargs['parent_lookup_board']
        board = get_object_or_404(Board, pk=board_pk)
        serializer.save(board=board)

class ListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = List.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(board__workspace__owner=profile) | Q(board__workspace__members=profile))
            & (Q(board__owner=profile) | Q(board__members=profile))
        )
        if not queryset.exists():
            raise Http404("No Lists matches the given query.")

        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.serializer_class = ListReadSerializer

        if self.action in ('create', 'update', 'delete'):
            self.serializer_class = ListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        board_pk = self.kwargs['parent_lookup_board']
        board = get_object_or_404(Board, pk=board_pk)
        serializer.save(board=board)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.serializer_class = TaskReadSerializer

        if self.action in ('create', 'update', 'delete'):
            self.serializer_class = TaskSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(list__board__workspace__owner=profile) | Q(list__board__workspace__members=profile))
            & (Q(list__board__owner=profile) | Q(list__board__members=profile))
        )
        if not queryset.exists():
            raise Http404("No Tasks matches the given query.")

        return queryset

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     # if not instance.viewers.filter(pk=request.user.pk).exists():
    #     #     instance.viewers.add(request.user)
    #     #     instance.save()
    #
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        list_pk = self.kwargs['parent_lookup_list']
        list_ = get_object_or_404(List, pk=list_pk)
        serializer.save(list=list_)


class CheckListViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CheckListReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CheckList.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.serializer_class = CheckListReadSerializer

        if self.action in ('create', 'update', 'delete'):
            self.serializer_class = CheckListSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = super().get_queryset().filter(
            (Q(task__list__board__workspace__owner=profile) | Q(task__list__board__workspace__members=profile))
            & (Q(task__list__board__owner=profile) | Q(task__list__board__members=profile))
        )
        if not queryset.exists():
            raise Http404("No Checklist matches the given query.")

        return queryset

    def perform_create(self, serializer):
        task_pk = self.kwargs['parent_lookup_task']
        task_obj = get_object_or_404(Task, pk=task_pk)
        serializer.save(task=task_obj)
