from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from src.management.models import Comment, DashboardProject, Group, Marker, Project, \
    ProjectMember, Status, Task
from src.users.models import Profile


class ProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'photo', 'banner_color_hex',)


class GroupCreateSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'color_hex', 'order', 'is_default')


class GroupUpdateSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'color_hex', 'order', 'is_default')


class GroupMoveSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('order',)


class MemberUpdateSerializer(ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ('groups',)


class StatusCreateSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ('name', 'category', 'order',)


class StatusMoveSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ('order',)


class MarkerCreateSerializer(ModelSerializer):
    class Meta:
        model = Marker
        fields = ('name', 'color_hex',)


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title', 'description',
            'start_date', 'end_date', 'duration',
            'priority', 'status', 'assignee',
            'markers', 'dependencies', 'order',
        )
        extra_kwargs = {
            'assignee': {'allow_null': True},
            'markers': {'default': []},
            'dependencies': {'default': []},
        }


class TaskMoveSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('status', 'order')


class ProjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'photo')


class DashboardProjectMoveSerializer(ModelSerializer):
    class Meta:
        model = DashboardProject
        fields = ('order',)
