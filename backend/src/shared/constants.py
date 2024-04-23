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
    class Name:
        CREATE_WORKSPACE_GROUP: Final[str] = 'Create workspace group'
        EDIT_WORKSPACE_GROUP: Final[str] = 'Edit workspace group'
        CHANGE_WORKSPACE_GROUP_PERMISSIONS: Final[str] = 'Change workspace group permission'

        EDIT_BOARD: Final[str] = 'Edit board'
        INVITE_MEMBERS: Final[str] = 'Invite members'
        EXPEL_MEMBERS: Final[str] = 'Expel members'
        EDIT_MEMBERS_PERMISSIONS: Final[str] = 'Edit members permissions'
        CREATE_LISTS: Final[str] = 'Create lists'
        EDIT_LISTS: Final[str] = 'Edit lists'
        DELETE_LISTS: Final[str] = 'Delete lists'
        CREATE_TASKS: Final[str] = 'Create tasks'
        EDIT_TASKS: Final[str] = 'Edit tasks'
        DELETE_TASKS: Final[str] = 'Delete tasks'
        ASSIGN_EXECUTORS_TO_TASKS: Final[str] = 'Assign executors to tasks'

    class Code:
        CREATE_WORKSPACE_GROUP: Final[str] = 'workspace_group_create'
        EDIT_WORKSPACE_GROUP: Final[str] = 'workspace_group_edit'
        CHANGE_WORKSPACE_GROUP_PERMISSIONS: Final[str] = 'workspace_group_permission_change'

        EDIT_BOARD: Final[str] = 'board_edit'
        INVITE_MEMBERS: Final[str] = 'board_members_invite'
        EXPEL_MEMBERS: Final[str] = 'board_members_expel'
        EDIT_MEMBERS_PERMISSIONS: Final[str] = 'board_members_edit_permissions'
        CREATE_LISTS: Final[str] = 'board_lists_create'
        EDIT_LISTS: Final[str] = 'board_lists_edit'
        DELETE_LISTS: Final[str] = 'board_lists_delete'
        CREATE_TASKS: Final[str] = 'board_tasks_create'
        EDIT_TASKS: Final[str] = 'board_tasks_edit'
        DELETE_TASKS: Final[str] = 'board_tasks_delete'
        ASSIGN_EXECUTORS_TO_TASKS: Final[str] = 'board_tasks_assign_executors'

    DATA: Final[tuple[str, str]] = [
        (Name.EDIT_BOARD, Code.EDIT_BOARD),
        (Name.INVITE_MEMBERS, Code.INVITE_MEMBERS),
        (Name.EXPEL_MEMBERS, Code.EXPEL_MEMBERS),
        (Name.EDIT_MEMBERS_PERMISSIONS, Code.EDIT_MEMBERS_PERMISSIONS),
        (Name.CREATE_LISTS, Code.CREATE_LISTS),
        (Name.EDIT_LISTS, Code.EDIT_LISTS),
        (Name.DELETE_LISTS, Code.DELETE_LISTS),
        (Name.CREATE_TASKS, Code.CREATE_TASKS),
        (Name.EDIT_TASKS, Code.EDIT_TASKS),
        (Name.DELETE_TASKS, Code.DELETE_TASKS),
        (Name.ASSIGN_EXECUTORS_TO_TASKS, Code.ASSIGN_EXECUTORS_TO_TASKS)
    ]
