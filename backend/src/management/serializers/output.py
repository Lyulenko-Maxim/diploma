from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.management.models import Comment, Dashboard, DashboardProject, Group, Marker, Permission, Project, \
    ProjectMember, \
    Status, Task
from src.users.models import Profile, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'deleted_at')


class ProfilePrivateSerializer(ModelSerializer):
    user = UserSerializer(read_only=True, )

    class Meta:
        model = Profile
        fields = (
            'id', 'user', 'username',
            'first_name', 'last_name', 'photo',
            'banner_color_hex', 'created_at', 'updated_at'
        )


class ProfilePublicSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'banner_color_hex')


class PermissionListSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'description', 'order')


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'order', 'is_default')


class GroupDetailSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'permissions', 'order', 'is_default')


class MemberListSerializer(ModelSerializer):
    profile = ProfilePublicSerializer(read_only=True)
    highest_group = SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ('id', 'profile', 'highest_group', 'created_at')

    @staticmethod
    def get_highest_group(obj: ProjectMember):
        return GroupListSerializer(instance=obj.highest_group).data


class MemberDetailSerializer(ModelSerializer):
    profile = ProfilePublicSerializer(read_only=True)
    groups = GroupListSerializer(read_only=True, many=True)

    class Meta:
        model = ProjectMember
        fields = ('id', 'profile', 'groups', 'created_at')


class MemberCurrentSerializer(ModelSerializer):
    profile = ProfilePublicSerializer(read_only=True)
    permissions = SerializerMethodField(read_only=True)
    highest_group = SerializerMethodField(read_only=True)
    is_owner = SerializerMethodField(read_only=True)
    class Meta:
        model = ProjectMember
        fields = ('id', 'profile', 'permissions', 'highest_group', 'is_owner')
    
    @staticmethod
    def get_is_owner(obj: ProjectMember):
        return obj.project.owner.id==obj.profile.id
        
    @staticmethod
    def get_permissions(obj: ProjectMember):
        return obj.permissions
	
    @staticmethod
    def get_highest_group(obj: ProjectMember):
        return GroupListSerializer(instance=obj.highest_group).data

class StatusListSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'order', 'category',)


class MarkerListSerializer(ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'color_hex', 'created_at')


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'owner',)


class TaskListSerializer(ModelSerializer):
    author = MemberListSerializer(read_only=True)
    assignee = MemberListSerializer(read_only=True)
    status = StatusListSerializer(read_only=True)
    markers = MarkerListSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'start_date', 'end_date', 'duration',
            'priority', 'status', 'author', 'assignee', 'markers',
            'created_at','updated_at'
        )


class TaskGanttListSerializer(ModelSerializer):
    author = MemberListSerializer(read_only=True)
    assignee = MemberListSerializer(read_only=True)
    dependencies = SerializerMethodField(read_only=True)
    status = StatusListSerializer(read_only=True)
    markers = MarkerListSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'start_date', 'end_date', 'duration',
            'priority', 'status', 'author', 'assignee', 'markers',
            'created_at', 'updated_at',
        )

    @staticmethod
    def get_dependencies(obj: Task):
        return TaskGanttListSerializer(instance=obj.dependencies, many=True).data


class TaskDetailSerializer(ModelSerializer):
    author = MemberListSerializer(read_only=True)
    assignee = MemberListSerializer(read_only=True)
    status = StatusListSerializer(read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)
    markers = MarkerListSerializer(read_only=True, many=True)
    dependencies = TaskListSerializer(read_only=True, many=True)
    available_dependencies = SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description',
            'start_date', 'end_date', 'duration',
            'priority', 'status',
            'author', 'assignee',
            'markers', 'dependencies', 'comments',
            'available_dependencies',
            'created_at', 'updated_at',
        )

    @staticmethod
    def get_available_dependencies(obj: Task):
        return TaskListSerializer(instance=obj.available_dependencies, many=True).data


class ProjectListSerializer(ModelSerializer):
    owner = SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'photo')

    def get_owner(self, obj):
        instance = ProjectMember.objects.filter(project=obj, profile=obj.owner).first()
        return MemberListSerializer(instance=instance, context=self.context).data


class DashboardProjectListSerializer(ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    current_member = SerializerMethodField(read_only=True)
    random_members = SerializerMethodField(read_only=True)
    members_count = SerializerMethodField(read_only=True)

    class Meta:
        model = DashboardProject
        fields = ('id', 'project', 'order', 'current_member', 'random_members', 'members_count',)

    def get_current_member(self, obj: DashboardProject):
        instance = (
            ProjectMember.objects
            .filter(project=obj.project, project__members=obj.dashboard.owner)
            .first()
        )
        return MemberListSerializer(instance=instance, context=self.context).data

    def get_random_members(self, obj):
        instance = ProjectMember.objects.filter(project=obj.project).order_by('?')[:3]
        return MemberListSerializer(instance=instance, many=True, context=self.context).data

    @staticmethod
    def get_members_count(obj):
        return obj.project.members.count()


class DashboardDetailSerializer(ModelSerializer):
    projects = DashboardProjectListSerializer(read_only=True, many=True, source='dashboardproject_set')

    class Meta:
        model = Dashboard
        fields = ('id', 'owner', 'projects',)


class TaskNotificationSerializer(ModelSerializer):
    subscribers = SerializerMethodField(read_only=True, )
    project = ProjectListSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'project', 'subscribers')

    @staticmethod
    def get_subscribers(obj):
        users = (
            User.objects
            .filter(profile__projects_memberships__in=obj.subscribers.all())
            .values_list('id', flat=True)
        )
        return list(map(str, list(users)))
