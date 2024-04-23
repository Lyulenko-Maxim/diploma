from rest_framework import serializers

from .models import Invitation
from ..management.serializers import WorkspaceReadSerializer
from ..users.serializers import ProfileSerializer


class InvitationReadSerializer(serializers.ModelSerializer):
    workspace = WorkspaceReadSerializer(read_only=True, required=False)
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ('id', 'workspace', 'sender', 'invited_at',)
