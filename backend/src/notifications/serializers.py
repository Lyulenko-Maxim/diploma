from rest_framework import serializers

from .models import Invitation
from ..users.serializers import ProfileSerializer


class InvitationReadSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ('id', 'project', 'sender', 'created_at',)
