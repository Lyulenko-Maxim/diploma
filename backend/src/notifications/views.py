from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Invitation
from .serializers import InvitationReadSerializer
from ..shared.serializers import EmptySerializer

User = get_user_model()


class InvitationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = InvitationReadSerializer

    def get_queryset(self):
        return (
            Invitation.objects
            .filter(Q(recipient=self.request.user.profile))
            .order_by('-invited_at')
        )

    def get_serializer_class(self):
        if self.action in ('accept', 'reject',):
            return EmptySerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post', ], url_path='accept')
    def accept(self, request, *args, **kwargs):
        with transaction.atomic():
            invitation = self.get_object()
            invitation.accept()
        return Response({'message': _('Invitation accepted')}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post', ], url_path='reject')
    def reject(self, request, *args, **kwargs):
        with transaction.atomic():
            invitation = self.get_object()
            invitation.reject()
        return Response({'message': _('Invitation rejected')}, status=status.HTTP_202_ACCEPTED)
