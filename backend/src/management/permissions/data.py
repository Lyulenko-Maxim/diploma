from typing import Final


class PermissionsDATA:
    class Name:
        ADMINISTRATOR: Final[str] = 'Администратор'
        MANAGE_PROJECT: Final[str] = 'Управление проектом'
        MANAGE_GROUPS: Final[str] = 'Управление группами'
        MANAGE_MEMBERS: Final[str] = 'Управление участниками'
        MANAGE_TASKS: Final[str] = 'Управление задачами'
        MANAGE_STATUSES: Final[str] = 'Управление статусами задач'
        MANAGE_MARKERS: Final[str] = 'Управление маркерами'
        MANAGE_COMMENTS: Final[str] = 'Управление комментариями'
        CREATE_COMMENTS: Final[str] = 'Комментировать задачи'
        CREATE_INVITATIONS: Final[str] = 'Создание приглашения'

    class Description:
        ADMINISTRATOR: Final[str] = \
            'Участники с данным правом имеют все права и обходят особые права и ограничения. Назначать это право опасно.'

        MANAGE_PROJECT: Final[str] = \
            'Дает участникам право управлять информацией о проекте.'

        MANAGE_GROUPS: Final[str] = \
            ('Позволяет участникам создавать новые группы и редактировать/перемещать/удалять существующие, '
             'которые находятся ниже, чем их самая высокая группа. '
             'Также это право позволяет назначать и удалять группы другим участникам, но только те группы, '
             'которые находятся ниже, чем их самая высокая группа')

        MANAGE_STATUSES: Final[str] = \
            'Позволяет участникам создавать новые статусы и редактировать/перемещать/удалять существующие.'

        MANAGE_MARKERS: Final[str] = \
            'Позволяет участникам создавать новые маркеры и редактировать/удалять существующие.'

        MANAGE_TASKS: Final[str] = \
            'Позволяет участникам создавать новые задачи и редактировать/удалять существующие.'

        MANAGE_COMMENTS: Final[str] = \
            'Позволяет участникам удалять комментарии других участников проекта.'

        CREATE_INVITATIONS: Final[str] = \
            'Позволяет приглашать других участников в проект.'

        MANAGE_MEMBERS: Final[str] = \
            'Позволяет исключать участников из проекта.'

        CREATE_COMMENTS: Final[str] = \
            'Позволяет участникам оставлять комментарии под задачами.'

    class Code:
        ADMINISTRATOR: Final[str] = 'admin'
        MANAGE_PROJECT: Final[str] = 'manage_project'
        MANAGE_GROUPS: Final[str] = 'manage_groups'
        MANAGE_MEMBERS: Final[str] = 'manage_members'
        MANAGE_TASKS: Final[str] = 'manage_tasks'
        MANAGE_STATUSES: Final[str] = 'manage_statuses'
        MANAGE_MARKERS: Final[str] = 'manage_markers'
        MANAGE_COMMENTS: Final[str] = 'manage_comments'
        CREATE_COMMENTS: Final[str] = 'create_comments'
        CREATE_INVITATIONS: Final[str] = 'create_invitations'

    class Order:
        ADMINISTRATOR: Final[int] = 0
        MANAGE_PROJECT: Final[int] = 1
        MANAGE_GROUPS: Final[int] = 2
        MANAGE_MEMBERS: Final[int] = 3
        MANAGE_TASKS: Final[int] = 4
        MANAGE_STATUSES: Final[int] = 5
        MANAGE_MARKERS: Final[int] = 6
        MANAGE_COMMENTS: Final[int] = 7
        CREATE_COMMENTS: Final[int] = 8
        CREATE_INVITATIONS: Final[int] = 9

    GROUPS = [
        "ADMINISTRATOR",
        "MANAGE_PROJECT",
        "MANAGE_TASKS",
        "MANAGE_MEMBERS",
        "MANAGE_GROUPS",
        "MANAGE_STATUSES",
        "MANAGE_MARKERS",
        "MANAGE_COMMENTS",
        "CREATE_COMMENTS",
        "CREATE_INVITATIONS",
    ]


PERMISSIONS_DATA: Final[list[tuple[str, str, str, int]]] = [
    (
        getattr(PermissionsDATA.Name, group),
        getattr(PermissionsDATA.Description, group),
        getattr(PermissionsDATA.Code, group),
        getattr(PermissionsDATA.Order, group)
    )
    for group in PermissionsDATA.GROUPS
]
