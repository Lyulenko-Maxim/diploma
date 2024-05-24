import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication

from .services import JWTService


class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация через JWT-токены.
    """

    def authenticate(self, request):
        User = get_user_model()
        access_token, _ = JWTService.get_tokens_from_request(request=request)

        # Если нет токена, продолжаем работу как анонимный пользователь
        if not access_token:
            return None

        # Пробуем получить пользователя из токена
        try:
            payload = JWTService.get_payload(access_token)
            user = User.objects.get(pk=payload['id'], email=payload['email'])
            return user, None

        # Если не удалось получить пользователя из токена,
        # продолжаем работу как анонимный пользователь
        except (jwt.DecodeError, KeyError, User.DoesNotExist):
            return None

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '401 Unauthenticated'
