from rest_framework import serializers

from .models import Comment, Dashboard, DashboardProject, Group, Marker, Permission, Project, ProjectMember, Status, \
    Task
from ..users.serializers import ProfileReadSerializer


class ProjectPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        project_pk = self.context.get('project_pk', None)
        queryset = super().get_queryset()
        if not project_pk or not queryset:
            return None
        return queryset.filter(project=project_pk)


class GroupPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        project_pk = self.context.get('project_pk', None)
        queryset = super().get_queryset()
        if not project_pk or not queryset:
            return None
        return queryset.filter(project=project_pk)


class TaskPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        project_pk = self.context.get('project_pk', None)
        instance: Task = self.context.get('instance', None)

        if instance:
            queryset = instance.valid_dependencies()
            return queryset

        queryset = super().get_queryset()

        if not project_pk or not queryset:
            return None

        return queryset.filter(project=project_pk)


class MarkerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'color_hex',)


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'color_hex', 'project',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'project': {'read_only': True, },
        }


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'code',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'name': {'read_only': True, },
            'code': {'read_only': True, },
        }


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'order',)


class ProjectMemberListSerializer(serializers.ModelSerializer):
    profile = ProfileReadSerializer(read_only=True)
    groups = GroupListSerializer(read_only=True, many=True)

    class Meta:
        model = ProjectMember
        fields = ('id', 'profile', 'groups', 'date_joined', 'deactivated',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'date_joined': {'read_only': True, },
            'groups': {'read_only': True, },
            'deactivated': {'read_only': True, },
        }


class ProjectMemberAssignSerializer(serializers.ModelSerializer):
    groups = ProjectPKRelatedField(queryset=Group.objects, many=True, )

    class Meta:
        model = ProjectMember
        fields = ('id', 'groups',)
        extra_kwargs = {
            'id': {'read_only': True, },
        }

    def get_permissions(self, obj):
        serializer = PermissionSerializer(instance=obj.get_permissions(), many=True, )
        return serializer.data


class ProjectMemberSerializer(serializers.ModelSerializer):
    profile = ProfileReadSerializer(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)
    groups = GroupListSerializer(read_only=True, many=True, )

    class Meta:
        model = ProjectMember
        fields = ('id', 'profile', 'date_joined', 'deactivated', 'groups', 'permissions',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'date_joined': {'read_only': True, },
            'groups': {'read_only': True, },
            'deactivated': {'read_only': True, },
        }

    def get_permissions(self, obj):
        serializer = PermissionSerializer(instance=obj.get_permissions(), many=True, )
        return serializer.data


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    # members = ProjectPKRelatedField(queryset=ProjectMember.objects, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'order', 'permissions',)
        extra_kwargs = {
            'id': {'read_only': True, },
        }


class RGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'order', 'project', 'permissions',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'name': {'read_only': True, },
            'color_hex': {'read_only': True, },
            'order': {'read_only': True, },
            'project': {'read_only': True, },
        }


class ProjectListSerializer(serializers.ModelSerializer):
    owner = ProfileReadSerializer(read_only=True, )

    class Meta:
        model = Project
        fields = ('id', 'name', 'slug', 'owner',)


class ProjectSerializer(serializers.ModelSerializer):
    # members = ProjectMemberSerializer(read_only=True, many=True, source='members_set')

    class Meta:
        model = Project
        fields = ('id', 'name', 'slug', 'description', 'owner',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'slug': {'read_only': True, },
            'owner': {'read_only': True, },
        }


class DashboardProjectSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True, )
    my_group = serializers.SerializerMethodField(read_only=True, )
    members = serializers.SerializerMethodField(read_only=True)
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DashboardProject
        fields = ('id', 'project', 'dashboard', 'order', 'my_group', 'members', 'members_count',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'project': {'read_only': True, },
            'dashboard': {'read_only': True, },
        }

    def get_my_group(self, obj):
        instance = (
            Group.objects
            .filter(project=obj.project, members__profile=obj.dashboard.owner)
            .order_by('order')
            .first()
        )
        return GroupSerializer(instance=instance).data

    def get_members(self, obj):
        instance = ProjectMember.objects.filter(project=obj.project)
        return ProjectMemberSerializer(instance=instance, many=True, context=self.context).data

    def get_members_count(self, obj):
        return obj.project.members.count()


class DashboardSerializer(serializers.ModelSerializer):
    projects = DashboardProjectSerializer(read_only=True, many=True, source='dashboardproject_set')

    class Meta:
        model = Dashboard
        fields = ('id', 'owner', 'projects',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'owner': {'read_only': True, },
        }


class CommentSerializer(serializers.ModelSerializer):
    owner = ProjectMemberSerializer(read_only=True)
    mentioned_members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'owner', 'created_at', 'last_edit', 'mentioned_members',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'created_at': {'read_only': True, },
            'last_edit': {'read_only': True, },
            'mentioned_members': {'read_only': True, },
        }

    def get_mentioned_members(self, obj):
        serializer = ProjectMemberSerializer(instance=obj.mentioned_members, many=True, )
        return serializer.data


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'name', 'order', 'category',)
        extra_kwargs = {
            'id': {'read_only': True, },
        }


class TaskWithoutDepSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    assignee = ProjectMemberSerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'key', 'status', 'title', 'description', 'priority', 'markers', 'due_date', 'created_at',
            'is_archived', 'project', 'author', 'assignee', 'comments', 'order',
        )
        extra_kwargs = {
            'id': {'read_only': True, },
            'key': {'read_only': True, },
            'created_at': {'read_only': True, },
            'is_archived': {'read_only': True, },
            'project': {'read_only': True, },
            'author': {'read_only': True, },
        }


class RTaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, )
    assignee = ProjectPKRelatedField(queryset=ProjectMember.objects)
    status = ProjectPKRelatedField(queryset=Status.objects)
    available_dependencies = serializers.SerializerMethodField(read_only=True)
    dependencies = TaskPKRelatedField(queryset=Task.objects, many=True, )
    parent = ProjectPKRelatedField(queryset=Task.objects, allow_null=True, )
    markers = ProjectPKRelatedField(queryset=Marker.objects, many=True, )

    class Meta:
        model = Task
        fields = (
            'id', 'key', 'status', 'title', 'description', 'priority', 'markers', 'due_date', 'created_at',
            'is_archived', 'project', 'author', 'assignee', 'parent', 'dependencies',
            'available_dependencies', 'comments', 'order',
        )
        extra_kwargs = {
            'id': {'read_only': True, },
            'key': {'read_only': True, },
            'created_at': {'read_only': True, },
            'is_archived': {'read_only': True, },
            'project': {'read_only': True, },
            'author': {'read_only': True, },
        }

    def get_available_dependencies(self, obj):
        serializer = TaskSerializer(instance=obj.available_dependencies(), many=True, )
        return serializer.data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description',)

# class BoardBackgroundSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BoardBackground
#         fields = ('id', 'image', 'color_hex',)
#
#     def validate(self, data):
#         image = data.get('image')
#         color_hex = data.get('color_hex')
#
#         if image and color_hex:
#             raise serializers.ValidationError(_('Only one of image or color can be provided.'))
#
#         if not image and not color_hex:
#             data['color_hex'] = Color.WHITE_HEX
#
#         return data
