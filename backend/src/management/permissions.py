from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from src.management.models import Permission, Project, ProjectMember
from src.shared.constants import Permissions

CODES = Permissions.Code


class ProjectPermissionFactory(BasePermission):
    AVAILABLE_CODES = (CODES.ADMINISTRATOR,)

    @staticmethod
    def _get_project(view) -> Project:
        project_pk = view.kwargs.get('project_pk', None)

        if not project_pk:
            project_pk = view.kwargs.get('pk', None)

        return get_object_or_404(Project, pk=project_pk)

    @staticmethod
    def _get_profile(request):
        return request.user.profile

    @staticmethod
    def _get_member(profile, project):
        return get_object_or_404(ProjectMember, project=project, profile=profile)

    def has_permission(self, request, view):
        profile = self._get_profile(request=request)

        project = self._get_project(view=view)
        member = self._get_member(profile=profile, project=project)

        if profile == project.owner:
            return True

        if not self.AVAILABLE_CODES:
            return False

        member_permissions = member.get_permissions()
        available_permissions = Permission.objects.filter(code__in=self.AVAILABLE_CODES)
        return any(permission in member_permissions for permission in available_permissions)

    def has_object_permission(self, request, view, obj):
        profile = self._get_profile(request=request)
        print(profile)
        project = obj if isinstance(obj, Project) else self._get_project(view=view)
        member = self._get_member(profile=profile, project=project)

        if hasattr(obj, 'owner') and isinstance(obj.owner, ProjectMember) and profile == obj.owner.profile:
            return True

        if not self.AVAILABLE_CODES:
            # only object owner has access
            return False

        if profile == project.owner:
            return True

        member_permissions = member.get_permissions()

        available_permissions = Permission.objects.filter(code__in=self.AVAILABLE_CODES)
        return any(permission in member_permissions for permission in available_permissions)

    @classmethod
    def create_permission(cls, perm_codes: tuple, clear_perms: bool = False):
        class CustomPermission(cls):
            if clear_perms:
                AVAILABLE_CODES = []
            else:
                AVAILABLE_CODES = cls.AVAILABLE_CODES + perm_codes

        return CustomPermission


def create_permission(perm_codes: tuple, clear_perms: bool = False):
    return ProjectPermissionFactory.create_permission(perm_codes=perm_codes, clear_perms=clear_perms)


CanUpdateProject = create_permission((CODES.UPDATE_PROJECT,))
CanDeleteProject = create_permission((CODES.DELETE_PROJECT,))

CanCreateStatus = create_permission((CODES.CREATE_STATUS,))
CanUpdateStatus = create_permission((CODES.UPDATE_STATUS,))
CanDeleteStatus = create_permission((CODES.DELETE_STATUS,))

CanCreateTask = create_permission((CODES.CREATE_TASK,))
CanUpdateTask = create_permission((CODES.UPDATE_TASK,))
CanDeleteTask = create_permission((CODES.DELETE_TASK,))
CanAssignTask = create_permission((CODES.ASSIGN_TASK,))

CanCreateMarker = create_permission((CODES.CREATE_MARKER,))
CanUpdateMarker = create_permission((CODES.UPDATE_MARKER,))
CanDeleteMarker = create_permission((CODES.DELETE_MARKER,))

CanCreateGroup = create_permission((CODES.CREATE_GROUP,))
CanUpdateGroup = create_permission((CODES.UPDATE_GROUP,))
CanDeleteGroup = create_permission((CODES.DELETE_GROUP,))
CanAssignGroup = create_permission((CODES.ASSIGN_GROUP,))
CanViewGroup = create_permission((
    CODES.VIEW_GROUP,
    CODES.CREATE_GROUP,
    CODES.UPDATE_GROUP,
    CODES.DELETE_GROUP,
))

CanInviteMember = create_permission((CODES.INVITE_MEMBER,))
CanExpelMember = create_permission((CODES.EXPEL_MEMBER,))

CanCreateComment = create_permission((CODES.CREATE_COMMENT,))
CanDeleteComment = create_permission((CODES.DELETE_COMMENT,))
CanUpdateComment = create_permission((CODES.CREATE_COMMENT,), True)
