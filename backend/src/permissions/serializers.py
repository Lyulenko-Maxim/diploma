from rest_framework import serializers

from src.permissions.models import Group, Permission


class WorkspaceMemberFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        workspace_pk = self.context.get('workspace_pk', None)
        queryset = super(WorkspaceMemberFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not workspace_pk or not queryset:
            return None
        return queryset.filter(workspace=workspace_pk)


class PermissionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'code',)


class GroupSerializer(serializers.ModelSerializer):
    from src.management.models import WorkspaceMember
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    members = WorkspaceMemberFilteredPrimaryKeyRelatedField(queryset=WorkspaceMember.objects, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'position', 'permissions', 'members',)


class GroupReadSerializer(serializers.ModelSerializer):
    from src.management.serializers import WorkspaceMemberReadSerializer
    members = WorkspaceMemberReadSerializer(many=True, read_only=True)
    permissions = PermissionReadSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'color_hex', 'position', 'workspace', 'permissions', 'members',)
