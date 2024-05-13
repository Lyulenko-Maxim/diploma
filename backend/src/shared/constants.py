from typing import Final
from django.utils.translation import gettext_lazy as _


class PrivacyType:
    PRIVATE: Final[str] = 'Private'
    PUBLIC: Final[str] = 'Public'
    TEAM: Final[str] = 'Team'

    CHOICES: Final[list[tuple[str, str]]] = [
        (PRIVATE.lower(), _(PRIVATE)),
        (PUBLIC.lower(), _(PUBLIC)),
        (TEAM.lower(), _(TEAM)),
    ]


class InvitationType:
    BOARD: Final[str] = 'Board'
    WORKSPACE: Final[str] = 'Workspace'

    CHOICES: Final[list[tuple[str, str]]] = [
        (BOARD.lower(), _(BOARD)),
        (WORKSPACE.lower(), _(WORKSPACE)),
    ]


class Color:
    WHITE_HEX: Final[str] = '#ffffff'
    BLACK_HEX: Final[str] = '#000000'


class InviteLimit:
    HOURS: Final[int] = 24
    COUNT: Final[int] = 2


class Permissions:
    class ContentType:
        PROJECT: Final[str] = 'Project'
        TASK: Final[str] = 'Task'
        STATUS: Final[str] = 'Status'
        MARKER: Final[str] = 'Marker'
        GROUP: Final[str] = 'Group'
        MEMBER: Final[str] = 'Member'
        INVITATION: Final[str] = 'Invitation'
        COMMENT: Final[str] = 'Comment'

    class ActionType:
        VIEW: Final[str] = 'View'
        CREATE: Final[str] = 'Create'
        UPDATE: Final[str] = 'Update'
        DELETE: Final[str] = 'Delete'
        ASSIGN: Final[str] = 'Assign'

    class Name:
        ADMINISTRATOR: Final[str] = 'Administrator'

        UPDATE_PROJECT: Final[str] = 'Update project'
        DELETE_PROJECT: Final[str] = 'Delete project'

        CREATE_STATUS: Final[str] = 'Create status'
        UPDATE_STATUS: Final[str] = 'Update status'
        DELETE_STATUS: Final[str] = 'Delete status'

        CREATE_MARKER: Final[str] = 'Create marker'
        UPDATE_MARKER: Final[str] = 'Update marker'
        DELETE_MARKER: Final[str] = 'Delete marker'

        CREATE_TASK: Final[str] = 'Create task'
        UPDATE_TASK: Final[str] = 'Update task'
        DELETE_TASK: Final[str] = 'Delete task'
        ASSIGN_TASK: Final[str] = 'Assign task to member'

        CREATE_GROUP: Final[str] = 'Create group'
        UPDATE_GROUP: Final[str] = 'Update group'
        DELETE_GROUP: Final[str] = 'Delete group'
        ASSIGN_GROUP: Final[str] = 'Assign group to member'
        VIEW_GROUP: Final[str] = 'View group'

        INVITE_MEMBER: Final[str] = 'Invite member'
        EXPEL_MEMBER: Final[str] = 'Expel member'

        CREATE_COMMENT: Final[str] = 'Create comment'
        UPDATE_COMMENT: Final[str] = 'Update comment'
        DELETE_COMMENT: Final[str] = 'Delete comment'

    class Code:
        ADMINISTRATOR: Final[str] = 'admin'

        UPDATE_PROJECT: Final[str] = 'project_update'
        DELETE_PROJECT: Final[str] = 'project_delete'

        CREATE_STATUS: Final[str] = 'status_create'
        UPDATE_STATUS: Final[str] = 'status_update'
        DELETE_STATUS: Final[str] = 'status_delete'

        CREATE_MARKER: Final[str] = 'marker_create'
        UPDATE_MARKER: Final[str] = 'marker_update'
        DELETE_MARKER: Final[str] = 'marker_delete'

        CREATE_TASK: Final[str] = 'task_create'
        UPDATE_TASK: Final[str] = 'task_update'
        DELETE_TASK: Final[str] = 'task_delete'
        ASSIGN_TASK: Final[str] = 'task_assign'

        CREATE_GROUP: Final[str] = 'group_create'
        UPDATE_GROUP: Final[str] = 'group_update'
        DELETE_GROUP: Final[str] = 'group_delete'
        ASSIGN_GROUP: Final[str] = 'group_assign'
        VIEW_GROUP: Final[str] = 'group_view'

        INVITE_MEMBER: Final[str] = 'member_invite'
        EXPEL_MEMBER: Final[str] = 'member_expel'

        CREATE_COMMENT: Final[str] = 'comment_create'
        DELETE_COMMENT: Final[str] = 'comment_delete'

    DATA: Final[tuple[str, str]] = [
        (Name.ADMINISTRATOR, Code.ADMINISTRATOR),
        (Name.UPDATE_PROJECT, Code.UPDATE_PROJECT),
        (Name.DELETE_PROJECT, Code.DELETE_PROJECT),
        (Name.CREATE_STATUS, Code.CREATE_STATUS),
        (Name.UPDATE_STATUS, Code.UPDATE_STATUS),
        (Name.DELETE_STATUS, Code.DELETE_STATUS),
        (Name.CREATE_MARKER, Code.CREATE_MARKER),
        (Name.UPDATE_MARKER, Code.UPDATE_MARKER),
        (Name.DELETE_MARKER, Code.DELETE_MARKER),
        (Name.CREATE_TASK, Code.CREATE_TASK),
        (Name.UPDATE_TASK, Code.UPDATE_TASK),
        (Name.DELETE_TASK, Code.DELETE_TASK),
        (Name.ASSIGN_TASK, Code.ASSIGN_TASK),
        (Name.CREATE_GROUP, Code.CREATE_GROUP),
        (Name.UPDATE_GROUP, Code.UPDATE_GROUP),
        (Name.DELETE_GROUP, Code.DELETE_GROUP),
        (Name.ASSIGN_GROUP, Code.ASSIGN_GROUP),
        (Name.VIEW_GROUP, Code.VIEW_GROUP),
        (Name.INVITE_MEMBER, Code.INVITE_MEMBER),
        (Name.EXPEL_MEMBER, Code.EXPEL_MEMBER),
        (Name.CREATE_COMMENT, Code.CREATE_COMMENT),
        (Name.DELETE_COMMENT, Code.DELETE_COMMENT),
    ]
