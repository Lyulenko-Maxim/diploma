from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import (BoardMemberViewSet, BoardViewSet, CheckListViewSet, ListViewSet, MarkerViewSet, TaskViewSet,
                    WorkspaceMemberViewSet,
                    WorkspaceViewSet, WorkspaceGroupViewSet)

router = ExtendedDefaultRouter()
workspaces_router = router.register(r'me/workspaces', WorkspaceViewSet, basename='workspaces')

workspaces_router.register(
    r'groups',
    WorkspaceGroupViewSet,
    basename='workspace-groups',
    parents_query_lookups=['workspace']
)

workspaces_router.register(
    r'members',
    WorkspaceMemberViewSet,
    basename='workspace-members',
    parents_query_lookups=['workspace']
)

board_router = workspaces_router.register(
    r'boards',
    BoardViewSet,
    basename='workspace-boards',
    parents_query_lookups=['workspace']
)

board_router.register(
    r'members',
    BoardMemberViewSet,
    basename='board-members',
    parents_query_lookups=['board__workspace', 'board']
)

board_router.register(
    r'markers',
    MarkerViewSet,
    basename='board-markers',
    parents_query_lookups=['board__workspace', 'board']
)

list_router = board_router.register(
    r'lists',
    ListViewSet,
    basename='board-lists',
    parents_query_lookups=['board__workspace', 'board']
)

task_router = list_router.register(
    r'tasks',
    TaskViewSet,
    basename='tasks',
    parents_query_lookups=['list__board__workspace', 'list__board', 'list']
)

task_router.register(
    r'checklists',
    CheckListViewSet,
    basename='task-checklists',
    parents_query_lookups=['task__list__board__workspace', 'task__list__board', 'task__list', 'task']
)

urlpatterns = router.urls

# workspace_router = DefaultRouter()
# workspace_router.register(r'workspaces', WorkspaceViewSet, basename='workspaces')
#
# group_router = DefaultRouter()
# group_router.register(r'groups', WorkspaceGroupViewSet, basename='groups')
#
# workspace_member_router = DefaultRouter()
# workspace_member_router.register(r'members', WorkspaceMemberViewSet, basename='members')
#
# board_router = DefaultRouter()
# board_router.register(r'boards', BoardViewSet, basename='boards')
#
# member_router = DefaultRouter()
# member_router.register(r'members', BoardMemberViewSet, basename='members')
#
# list_router = DefaultRouter()
# list_router.register(r'lists', ListViewSet, basename='lists')
#
# task_router = DefaultRouter()
# task_router.register(r'tasks', TaskViewSet, basename='tasks')
#
# urlpatterns = [
#     path('me/', include(workspace_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/', include(board_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/', include(group_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/', include(workspace_member_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/boards/<uuid:board_pk>/', include(member_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/boards/<uuid:board_pk>/', include(list_router.urls)),
#     path('me/workspaces/<uuid:workspace_pk>/boards/<uuid:board_pk>/lists/<uuid:list_pk>/', include(task_router.urls)),
# ]
