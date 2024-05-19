# from rest_framework import serializers
#
# from .models import Comment, Dashboard, DashboardProject, Group, Marker, Permission, Project, ProjectMember, Status, \
#     Task, User
# from ..users.serializers import ProfileReadSerializer
#
#
# class MoveSerializer(serializers.Serializer):
#     order = serializers.IntegerField(required=True)
#
#     def validate(self, attrs):
#         order = attrs.get('order')
#         if order < 0:
#             raise serializers.ValidationError({'error': 'Порядок не может быть меньше, чем 0.'})
#         return attrs
#
#
# class ProjectPKRelatedField(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         project_pk = self.context.get('project_pk', None)
#         queryset = super().get_queryset()
#         if not project_pk or not queryset:
#             return None
#         return queryset.filter(project=project_pk)
#
#
# class GroupPKRelatedField(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         project_pk = self.context.get('project_pk', None)
#         queryset = super().get_queryset()
#         if not project_pk or not queryset:
#             return None
#         return queryset.filter(project=project_pk)
#
#
# class TaskPKRelatedField(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         project_pk = self.context.get('project_pk', None)
#         instance: Task = self.context.get('instance', None)
#
#         if instance:
#             queryset = instance.valid_dependencies
#             return queryset
#
#         queryset = super().get_queryset()
#
#         if not project_pk or not queryset:
#             return None
#
#         return queryset.filter(project=project_pk)
#
#
# class MarkerReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Marker
#         fields = ('id', 'name', 'color_hex',)
#
#
# class MarkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Marker
#         fields = ('id', 'name', 'color_hex', 'project',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'project': {'read_only': True, },
#         }
#
#
# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = ('id', 'name', 'code',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'name': {'read_only': True, },
#             'code': {'read_only': True, },
#         }
#
#
# class GroupListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('id', 'name', 'color_hex', 'order',)
#
#
# class ProjectMemberListSerializer(serializers.ModelSerializer):
#     profile = ProfileReadSerializer(read_only=True)
#     groups = GroupListSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = ProjectMember
#         fields = ('id', 'profile', 'groups', 'deactivated',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'groups': {'read_only': True, },
#             'deactivated': {'read_only': True, },
#         }
#
#
# class ProjectMemberAssignSerializer(serializers.ModelSerializer):
#     groups = ProjectPKRelatedField(queryset=Group.objects, many=True, )
#
#     class Meta:
#         model = ProjectMember
#         fields = ('id', 'groups',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#         }
#
#     def get_permissions(self, obj):
#         serializer = PermissionSerializer(instance=obj.get_permissions(), many=True, )
#         return serializer.data
#
#
# class ProjectMemberSerializer(serializers.ModelSerializer):
#     profile = ProfileReadSerializer(read_only=True)
#     groups = GroupListSerializer(read_only=True, many=True, )
#     is_project_owner = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = ProjectMember
#         fields = ('id', 'profile', 'is_project_owner', 'created_at', 'deactivated', 'groups', 'permissions',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'created_at': {'read_only': True, },
#             'groups': {'read_only': True, },
#             'deactivated': {'read_only': True, },
#         }
#
#     def get_is_project_owner(self, obj: ProjectMember):
#         return obj.project.owner == obj.profile
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
#
#     # members = ProjectPKRelatedField(queryset=ProjectMember.objects, many=True)
#
#     class Meta:
#         model = Group
#         fields = ('id', 'name', 'color_hex', 'order', 'permissions',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#         }
#
#
# class RGroupSerializer(serializers.ModelSerializer):
#     permissions = PermissionSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Group
#         fields = ('id', 'name', 'color_hex', 'order', 'project', 'permissions',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'name': {'read_only': True, },
#             'color_hex': {'read_only': True, },
#             'order': {'read_only': True, },
#             'project': {'read_only': True, },
#         }
#
#
# class ProjectListSerializer(serializers.ModelSerializer):
#     owner = ProfileReadSerializer(read_only=True, )
#
#     class Meta:
#         model = Project
#         fields = ('id', 'name', 'owner',)
#
#
# class ProjectSerializer(serializers.ModelSerializer):
#     # members = ProjectMemberSerializer(read_only=True, many=True, source='members_set')
#
#     class Meta:
#         model = Project
#         fields = ('id', 'name', 'description', 'owner',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'owner': {'read_only': True, },
#         }
#
#
# class DashboardProjectMoveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DashboardProject
#         fields = ('order',)
#
#
# class DashboardProjectSerializer(serializers.ModelSerializer):
#     project = ProjectListSerializer(read_only=True, )
#     my_group = serializers.SerializerMethodField(read_only=True, )
#     members = serializers.SerializerMethodField(read_only=True)
#     members_count = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = DashboardProject
#         fields = ('id', 'project', 'dashboard', 'order', 'my_group', 'members', 'members_count',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'project': {'read_only': True, },
#             'dashboard': {'read_only': True, },
#         }
#
#     def get_my_group(self, obj):
#         instance = (
#             Group.objects
#             .filter(project=obj.project, members__profile=obj.dashboard.owner)
#             .order_by('order')
#             .first()
#         )
#         return GroupSerializer(instance=instance).data
#
#     def get_members(self, obj):
#         instance = ProjectMember.objects.filter(project=obj.project)
#         return ProjectMemberSerializer(instance=instance, many=True, context=self.context).data
#
#     def get_members_count(self, obj):
#         return obj.project.members.count()
#
#
# class DashboardSerializer(serializers.ModelSerializer):
#     projects = DashboardProjectSerializer(read_only=True, many=True, source='dashboardproject_set')
#
#     class Meta:
#         model = Dashboard
#         fields = ('id', 'owner', 'projects',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'owner': {'read_only': True, },
#         }
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     owner = ProjectMemberSerializer(read_only=True)
#
#     # mentioned_members = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'content', 'owner', 'created_at', 'updated_at',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'created_at': {'read_only': True, },
#             'updated_at': {'read_only': True, },
#             'mentioned_members': {'read_only': True, },
#         }
#
#     # def get_mentioned_members(self, obj):
#     #     serializer = ProjectMemberSerializer(instance=obj.mentioned_members, many=True, )
#     #     return serializer.data
#
#
# class StatusSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Status
#         fields = ('id', 'name', 'order', 'category',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#         }
#
#
# class StatusMoveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Status
#         fields = ('order',)
#
#
# class TaskWithoutDepSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(read_only=True, many=True)
#     assignee = ProjectMemberSerializer(read_only=True)
#     status = StatusSerializer(read_only=True)
#
#     class Meta:
#         model = Task
#         fields = (
#             'id', 'status', 'title', 'description', 'priority', 'markers', 'due_date', 'created_at',
#             'is_archived', 'project', 'author', 'assignee', 'comments', 'order',
#         )
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'created_at': {'read_only': True, },
#             'is_archived': {'read_only': True, },
#             'project': {'read_only': True, },
#             'author': {'read_only': True, },
#         }
#
#
# class InputTaskSerializer(serializers.ModelSerializer):
#     assignee = ProjectPKRelatedField(queryset=ProjectMember.objects, )
#     status = ProjectPKRelatedField(queryset=Status.objects, )
#     dependencies = TaskPKRelatedField(queryset=Task.objects, many=True, default=[], )
#     markers = ProjectPKRelatedField(queryset=Marker.objects, many=True, default=[], )
#
#     class Meta:
#         model = Task
#         exclude = (
#             'id', 'order', 'author', 'project', 'subscribers',
#         )
#
# class MemberListSerializer(serializers.ModelSerializer):
#     profile = ProfileReadSerializer(read_only=True)
#     groups = GroupListSerializer(read_only=True, many=True, )
#     is_project_owner = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = ProjectMember
#         fields = ('id', 'profile', 'is_project_owner', 'created_at',)
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'created_at': {'read_only': True, },
#             'groups': {'read_only': True, },
#             'deactivated': {'read_only': True, },
#         }
#
#
# class TaskDetailSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(read_only=True, many=True)
#     author = ProjectMemberSerializer(read_only=True)
#     class Meta:
#         model = Task
#         fields = (
#             'id', 'title', 'description',
#             'start_date', 'end_date', 'duration',
#             'priority', 'status',
#             'author', 'assignee',
#             'markers', 'dependencies', 'comments',
#             'available_dependencies'
#         )
#
#
# class OutputTaskSerializer(serializers.ModelSerializer):
#     assignee = ProjectPKRelatedField(queryset=ProjectMember.objects, )
#     status = ProjectPKRelatedField(queryset=Status.objects, )
#     dependencies = TaskPKRelatedField(queryset=Task.objects, many=True, default=[], )
#     markers = ProjectPKRelatedField(queryset=Marker.objects, many=True, default=[], )
#
#     class Meta:
#         model = Task
#         exclude = (
#             'id', 'order', 'author', 'project', 'subscribers', 'parent'
#         )
#
#
# class RTaskSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True, default=[], )
#     assignee = ProjectMemberSerializer(read_only=True)
#     author = ProjectMemberSerializer(read_only=True)
#     status = ProjectPKRelatedField(queryset=Status.objects, )
#     available_dependencies = serializers.SerializerMethodField(read_only=True, )
#     dependencies = TaskPKRelatedField(queryset=Task.objects, many=True, default=[], )
#     markers = ProjectPKRelatedField(queryset=Marker.objects, many=True, default=[], )
#
#     class Meta:
#         model = Task
#         fields = (
#             'id', 'status', 'title', 'description', 'priority', 'markers', 'due_date', 'created_at',
#             'is_archived', 'project', 'author', 'assignee', 'dependencies',
#             'available_dependencies', 'comments', 'order',
#         )
#         extra_kwargs = {
#             'id': {'read_only': True, },
#             'created_at': {'read_only': True, },
#             'is_archived': {'read_only': True, },
#             'project': {'read_only': True, },
#             'author': {'read_only': True, },
#         }
#
#     def get_available_dependencies(self, obj):
#         serializer = TaskSerializer(instance=obj.available_dependencies, many=True, )
#         return serializer.data
#
#
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ('id', 'title', 'description',)
#
#
# class TaskMoveSerializer(serializers.ModelSerializer):
#     status = ProjectPKRelatedField(queryset=Status.objects, )
#
#     class Meta:
#         model = Task
#         fields = ('status', 'order')
#
#
# class TaskAssignSerializer(serializers.ModelSerializer):
#     assignee = ProjectPKRelatedField(queryset=ProjectMember.objects, )
#
#     class Meta:
#         model = Task
#         fields = ('assignee',)
#
#
# class TaskNotificationSerializer(serializers.ModelSerializer):
#     subscribers = serializers.SerializerMethodField(read_only=True, )
#
#     class Meta:
#         model = Task
#         fields = ('id', 'title', 'subscribers')
#
#     def get_subscribers(self, obj):
#         users = (
#             User.objects
#             .filter(profile__projects_memberships__in=obj.subscribers.all())
#             .values_list('id', flat=True)
#         )
#         return list(map(str, list(users)))
