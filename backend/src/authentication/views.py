import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer
from .utils import check_activation_link, check_credentials, login, logout, send_activation_email
from ..users.permissions import IsAnonymous
from ..users.tasks import delete_account_task
from ..users.utils import get_user_deletion_task_id, safe_revoke

User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymous]

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user)

        user.deleted_at = timezone.now()
        user.delete_id = uuid.uuid4()
        user.save()

        delete_account_task.apply_async(
            kwargs={'user_id': user.id},
            eta=user.deleted_at + timedelta(minutes=int(settings.USER_ACCOUNT_DELETE_AFTER_REGISTER_MINUTES)),
            task_id=get_user_deletion_task_id(user),
        )


class ActivateView(APIView):
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        user = check_activation_link(self.kwargs.get('token'))

        if not user:
            return Response(data={'error': 'Невалидная ссылка активации аккаунта.'}, status=status.HTTP_404_NOT_FOUND)

        result = safe_revoke(user)

        if not result:
            return Response(data={'error': 'Невалидная ссылка активации аккаунта.'}, status=status.HTTP_404_NOT_FOUND)

        user.deleted_at = None
        user.delete_id = None
        user.is_active = True
        user.is_verified = True
        user.save(update_fields=['is_active', 'is_verified', 'deleted_at', 'delete_id'])

        return Response(
            data={'success': 'Успешная активация аккаунта.\nПожалуйста, авторизуйтесь используя свои учетные данные.'},
            status=status.HTTP_200_OK
        )


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.pop('password')

        user, error_message = check_credentials(email=email, password=password)

        if not user:
            raise AuthenticationFailed(
                {'error': _('Неверный логин или пароль.\nПожалуйста, проверьте введенные учетные данные.')}
            )

        return login(user=user, message='Успешная авторизация.', status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return logout(message='Успешный выход.', status=status.HTTP_200_OK)
