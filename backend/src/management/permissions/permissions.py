from rest_framework.permissions import BasePermission

from src.management.models import Comment, Project, ProjectMember
from src.management.permissions import PermissionsDATA

CODES = PermissionsDATA.Code


class IsProjectOwner(BasePermission):
    message = 'У вас недостаточно прав для совершения данного действия.'
    code = 403

    def has_permission(self, request, view):
        profile = request.user.profile
        project_pk = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        project = Project.objects.current_or_none(pk=project_pk, request=request)
        if not project:
            return False
        return profile == project.owner


class IsProjectMember(BasePermission):
    message = 'Не найдено ни одного проекта по вашему запросу.'
    code = 404

    def has_object_permission(self, request, view, obj):
        project_pk = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        project = Project.objects.current_or_none(pk=project_pk, request=request)
        return True if project else False

    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        project = Project.objects.current_or_none(pk=project_pk, request=request)

        return True if project else False


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Comment):
        if obj.owner.profile.user == request.user:
            return True

        return False


class BaseProjectPermission(BasePermission):
    message = 'У вас недостаточно прав для совершения данного действия.'
    code = 403
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
    )

    @staticmethod
    def _get_project(view) -> Project | None:
        project_pk = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        return Project.objects.filter(pk=project_pk).first()

    @staticmethod
    def _get_member(project, request) -> ProjectMember | None:
        return ProjectMember.objects.filter(project=project, profile__user=request.user).first()

    def _check_perms(self, member: ProjectMember):
        member_permissions_codes = member.permissions
        return any(code in member_permissions_codes for code in self.AVAILABLE_CODES)

    # def has_permission(self, request, view):
    #     project = self._get_project(view)
    #     if not project:
    #         return False
    #
    #     if project.owner.user == request.user:
    #         return True
    #
    #     member = self._get_member(project, request)
    #     return self._check_perms(member=member) if member else False

    def has_object_permission(self, request, view, obj):
        project = self._get_project(view)
        if not project:
            return False

        if project.owner.user == request.user:
            return True

        member = self._get_member(project, request)
        return self._check_perms(member=member) if member else False


class IsProjectManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_PROJECT,
    )


class IsTaskManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_TASKS,
    )


class IsGroupManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_GROUPS,
    )


class IsMemberManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_MEMBERS,
    )


class IsStatusManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_STATUSES,
    )


class IsMarkerManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_MARKERS,
    )


class IsCommentManager(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.MANAGE_COMMENTS,
    )


class IsCommentCreator(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.CREATE_COMMENTS,
    )


class IsInvitationCreator(BaseProjectPermission):
    AVAILABLE_CODES = (
        CODES.ADMINISTRATOR,
        CODES.CREATE_INVITATIONS,
    )

#
# class ProjectPermissionFactory(BasePermission):
#     AVAILABLE_CODES = (CODES.ADMINISTRATOR,)
#
#     @staticmethod
#     def _get_project(view) -> Project:
#         project_pk = view.kwargs.get('project_pk') or view.kwargs.get('pk')
#         return get_object_or_404(Project, pk=project_pk)
#
#     @staticmethod
#     def _get_profile(request):
#         return request.user.profile
#
#     @staticmethod
#     def _get_member(profile, project):
#         return get_object_or_404(ProjectMember, project=project, profile=profile)
#
#     def _has_permission(self, member, project):
#         if member.profile == project.owner:
#             return True
#
#         if member.deactivated:
#             return False
#
#         if not self.AVAILABLE_CODES:
#             return False
#
#         member_permissions = member.permissions()
#         available_permissions = Permission.objects.filter(code__in=self.AVAILABLE_CODES)
#         return any(permission in member_permissions for permission in available_permissions)
#
#     def has_permission(self, request, view):
#         profile = self._get_profile(request=request)
#         project = self._get_project(view=view)
#         member = self._get_member(profile=profile, project=project)
#         return self._has_permission(member=member, project=project)
#
#     def has_object_permission(self, request, view, obj):
#         profile = self._get_profile(request=request)
#         project = obj if isinstance(obj, Project) else self._get_project(view=view)
#         member = self._get_member(profile=profile, project=project)
#         action = view.action
#
#         if isinstance(obj, Comment):
#             result = self._can_manage_comment(member=member, comment=obj, action=action)
#             if result is not None:
#                 return result
#
#         if isinstance(obj, Task):
#             result = self._can_manage_task(member=member, task=obj, action=action)
#             if result is not None:
#                 return result
#
#         return self._has_permission(member=member, project=project)
#
#     @staticmethod
#     def _can_manage_comment(member, comment, action):
#         if member.deactivated:
#             return None
#
#         if action in ('update', 'partial_update'):
#             return member == comment.owner
#
#         if action == 'destroy' and member == comment.owner:
#             return True
#
#         return None
#
#     @staticmethod
#     def _can_manage_task(member, task, action):
#         if member.deactivated:
#             return None
#
#         if action in ('update', 'partial_update', 'destroy', 'assign', 'move') and member == task.author:
#             return True
#
#         if action == 'move' and task.assignee and member == task.assignee:
#             return True
#
#         return None
#
#     @classmethod
#     def create_permission(cls, perm_codes: tuple, clear_perms: bool = False):
#         class CustomPermission(cls):
#             AVAILABLE_CODES = [] if clear_perms else cls.AVAILABLE_CODES + perm_codes
#
#         return CustomPermission
#
#
# def create_permission(perm_codes: tuple, clear_perms: bool = False):
#     return ProjectPermissionFactory.create_permission(perm_codes=perm_codes, clear_perms=clear_perms)
#
#
# CanUpdateProject = create_permission((CODES.UPDATE_PROJECT,))
#
# CanCreateStatus = create_permission((CODES.CREATE_STATUS,))
# CanUpdateStatus = create_permission((CODES.UPDATE_STATUS,))
# CanDeleteStatus = create_permission((CODES.DELETE_STATUS,))
# CanMoveStatus = create_permission((CODES.CREATE_STATUS, CODES.UPDATE_STATUS,))
#
# CanCreateTask = create_permission((CODES.CREATE_TASK,))
# CanUpdateTask = create_permission((CODES.UPDATE_TASK,))
# CanDeleteTask = create_permission((CODES.DELETE_TASK,))
# CanAssignTask = create_permission((CODES.ASSIGN_TASK,))
# CanMoveTask = create_permission((CODES.MOVE_TASK, CODES.UPDATE_TASK,))
#
# CanCreateMarker = create_permission((CODES.CREATE_MARKER,))
# CanUpdateMarker = create_permission((CODES.UPDATE_MARKER,))
# CanDeleteMarker = create_permission((CODES.DELETE_MARKER,))
#
# CanCreateGroup = create_permission((CODES.CREATE_GROUP,))
# CanUpdateGroup = create_permission((CODES.UPDATE_GROUP,))
# CanDeleteGroup = create_permission((CODES.DELETE_GROUP, CODES.UPDATE_GROUP,))
# CanAssignGroup = create_permission((CODES.ASSIGN_GROUP,))
# CanMoveGroup = create_permission((CODES.CREATE_GROUP, CODES.UPDATE_GROUP,))
#
# CanViewGroup = create_permission((
#     CODES.CREATE_GROUP,
#     CODES.UPDATE_GROUP,
#     CODES.DELETE_GROUP,
# ))
#
# CanInviteMember = create_permission((CODES.INVITE_MEMBER,))
# CanExpelMember = create_permission((CODES.EXPEL_MEMBER,))
#
# CanCreateComment = create_permission((CODES.CREATE_COMMENT,))
# CanDeleteComment = create_permission((CODES.DELETE_COMMENT,))
# CanUpdateComment = create_permission((CODES.CREATE_COMMENT,), True)
