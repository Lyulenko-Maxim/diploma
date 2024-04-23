import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Profile, ProfilePhoto
from .serializers import (
    ChangePasswordSerializer, ProfilePhotoReadSerializer, ProfilePhotoSerializer, ProfileSerializer,
    UserSerializer
)

from .utils import create_account_deletion_request, get_user_deletion_task_id, safe_revoke
from ..shared.serializers import EmailSerializer, EmptySerializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('account',):
            self.serializer_class = UserSerializer

        if self.action in ('change_email',):
            self.serializer_class = EmailSerializer

        if self.action in ('change_password',):
            self.serializer_class = ChangePasswordSerializer

        if self.action in ('delete_account', 'restore_account',):
            self.serializer_class = EmptySerializer

        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='account')
    def account(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='account/change-email', serializer_class=UserSerializer)
    def change_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        new_email = serializer.validated_data['email']

        if User.objects.filter(email=new_email).exists():
            return Response({'error': _('This email address is taken by another user')})

        return Response({'message': 'Профиль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path='account/change-email', serializer_class=UserSerializer)
    def confirm_new_email(self, request):
        user = request.user

        user.email, user.new_email = user.new_email, None

        return Response({'message': 'Профиль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path='account/change-password')
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        return Response(data={'success': _('Password changed')}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='account/delete')
    def delete_account(self, request, *args, **kwargs):
        user = self.request.user

        if user.deleted_at:
            return Response(data={'error': _('Deletion request is already active')}, status=status.HTTP_403_FORBIDDEN)

        user.deleted_at = timezone.now()
        user.delete_id = uuid.uuid4()
        user.save()

        create_account_deletion_request(user)
        from core.celery import debug_task
        debug_task.delay()
        return Response(data={'success': 'Deletion request accepted'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], url_path='account/restore')
    def restore_account(self, request, *args, **kwargs):
        user = self.request.user
        result = safe_revoke(user)

        if not result:
            return Response(data={'error': 'Account has already been deleted'}, status=status.HTTP_400_BAD_REQUEST)

        user.deleted_at = None
        user.delete_id = None
        user.save()

        response = Response(data={'message': _("Successful account restore")}, status=status.HTTP_200_OK, )
        return response


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     if self.action in ('update', 'partial_update',):
    #         self.serializer_class = ProfilePhotoSerializer
    #
    #     super().get_serializer_class()


class ProfilePhotoViewSet(ModelViewSet):
    queryset = ProfilePhoto.objects.all()

    def get_serializer_class(self):
        if self.action in ('create',):
            self.serializer_class = ProfilePhotoSerializer
        else:
            self.serializer_class = ProfilePhotoReadSerializer
