from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    CommentViewSet, DashboardViewSet, GroupViewSet, ProjectMemberViewSet,
    ProjectViewSet,
    MarkerViewSet,
    StatusViewSet,
    TaskViewSet,
)

dashboard_router = DefaultRouter()
dashboard_router.register(r'', DashboardViewSet, basename='dashboard')

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'members', ProjectMemberViewSet, basename='project-members')
project_router.register(r'statuses', StatusViewSet, basename='project-statuses')
project_router.register(r'markers', MarkerViewSet, basename='project-markers')
project_router.register(r'groups', GroupViewSet, basename='project-groups')
project_router.register(r'tasks', TaskViewSet, basename='project-tasks')

task_router = routers.NestedSimpleRouter(project_router, r'tasks', lookup='task')
task_router.register(r'comments', CommentViewSet, basename='project-task-comments')

group_router = routers.NestedSimpleRouter(project_router, r'groups', lookup='group')
group_router.register(r'permissions', GroupViewSet, basename='project-groups')

urlpatterns = [
    path(r'', include(dashboard_router.urls)),
    path(r'dashboard/', include(router.urls)),
    path(r'dashboard/', include(project_router.urls)),
    path(r'dashboard/', include(task_router.urls)),
]
