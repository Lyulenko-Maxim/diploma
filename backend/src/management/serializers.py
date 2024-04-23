from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from src.shared.constants import Color
from src.shared.serializers import CurrentProfileDefault
from .models import Board, BoardMember, Check, CheckList, Comment, List, Permission, Task, Workspace, WorkspaceMember
from .models import BoardBackground, Marker
from ..permissions.models import Group
from ..users.serializers import ProfileReadSerializer, ProfileSerializer


class BoardBackgroundReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardBackground
        fields = ('id', 'image', 'color_hex',)


class BoardBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardBackground
        fields = ('id', 'image', 'color_hex',)

    def validate(self, data):
        image = data.get('image')
        color_hex = data.get('color_hex')

        if image and color_hex:
            raise serializers.ValidationError(_('Only one of image or color can be provided.'))

        if not image and not color_hex:
            data['color_hex'] = Color.WHITE_HEX

        return data


class MarkerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'color_hex',)


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'color_hex', 'board',)


class CheckReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'title', 'deadline', 'is_completed', 'executors',)


class CheckListReadSerializer(serializers.ModelSerializer):
    checks = CheckReadSerializer(many=True, read_only=True)

    class Meta:
        model = CheckList
        fields = ('id', 'name', 'checks')


class CheckListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckList
        fields = ('id', 'name',)


class BoardMemberReadSerializer(serializers.ModelSerializer):
    member = ProfileSerializer()

    class Meta:
        model = BoardMember
        fields = ('id', 'member', 'date_joined',)


class CommentReadSerializer(serializers.ModelSerializer):
    sender = BoardMemberReadSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'sender',)


class TaskReadSerializer(serializers.ModelSerializer):
    check_lists = CheckListReadSerializer(many=True, read_only=True, source='checklist_set')
    comments = CommentReadSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Task
        fields = ('id', 'title', 'owner', 'list', 'check_lists', 'description', 'deadline', 'created_at', 'is_archived',
                  'comments')


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentProfileDefault())

    class Meta:
        model = Task
        fields = ('id', 'title', 'owner', 'description',)


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'order',)


class ListReadSerializer(serializers.ModelSerializer):
    tasks = TaskReadSerializer(many=True, source='task_set')

    class Meta:
        model = List
        fields = ('id', 'name', 'order', 'tasks',)


class BoardMemberPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = BoardMember
        fields = ('permissions',)

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        instance.permissions.set(permissions_data)
        return instance


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentProfileDefault())

    class Meta:
        model = Board
        fields = ('id', 'name', 'description', 'privacy', 'background', 'owner', 'members',)


class BoardReadSerializer(serializers.ModelSerializer):
    lists = ListReadSerializer(many=True, )
    members = ProfileReadSerializer(many=True, )
    markers = MarkerReadSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = (
            'id', 'name', 'description', 'privacy', 'workspace', 'background', 'owner', 'members',
            'lists', 'markers',
        )


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentProfileDefault())

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'description', 'owner',)


class WorkspaceMemberReadSerializer(serializers.ModelSerializer):
    member = ProfileReadSerializer()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = WorkspaceMember
        fields = ('id', 'member', 'date_joined', 'groups', 'permissions')

    def get_permissions(self, obj):
        from src.permissions.serializers import PermissionReadSerializer
        permission_serializer = PermissionReadSerializer(instance=obj.get_permissions(), many=True)
        return permission_serializer.data


class WorkspaceReadSerializer(serializers.ModelSerializer):
    from ..permissions.serializers import GroupReadSerializer
    members = WorkspaceMemberReadSerializer(many=True, read_only=True, source='workspacemember_set')
    groups = GroupReadSerializer(many=True, read_only=True, )
    boards = BoardReadSerializer(many=True, read_only=True, source='board_set')
    owner = ProfileReadSerializer(read_only=True)

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'description', 'owner', 'groups', 'members', 'boards')


class WorkspaceGroupFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        workspace_pk = self.context.get('workspace_pk', None)
        queryset = super(WorkspaceGroupFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not workspace_pk or not queryset:
            return None
        return queryset.filter(workspace=workspace_pk)


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    groups = WorkspaceGroupFilteredPrimaryKeyRelatedField(queryset=Group.objects, many=True)

    class Meta:
        model = WorkspaceMember
        fields = ('id', 'groups',)


class PrivateBoardReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description', 'privacy',)
