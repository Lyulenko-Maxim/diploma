from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from rest_framework.request import Request

from django.conf import settings

User = get_user_model()


class JWTService:
    @staticmethod
    def generate_tokens(user: User) -> tuple[str | bytes, str | bytes]:
        """Генерирует access token и refresh токены для заданного пользователя."""

        access_token_payload = {
            'id': str(user.id),
            'email': user.email,
            'iat': datetime.timestamp(datetime.now()),
            'exp': datetime.utcnow() + timedelta(minutes=float(settings.JWT_ACCESS_TOKEN_EXP_MINUTES)),
        }

        refresh_token_payload = {
            'id': str(user.id),
            'email': user.email,
            'iat': datetime.timestamp(datetime.now()),
            'exp': datetime.utcnow() + timedelta(days=float(settings.JWT_REFRESH_TOKEN_EXP_DAYS)),
        }

        access_token = jwt.encode(
            payload=access_token_payload,
            key=settings.JWT_SIGNING_KEY,
            algorithm='HS256',
            headers={'typ': 'JWT', },
        )

        refresh_token = jwt.encode(
            payload=refresh_token_payload,
            key=settings.JWT_SIGNING_KEY,
            algorithm='HS256',
            headers={'typ': 'JWT', },
        )
        return access_token, refresh_token

    @staticmethod
    def get_tokens_from_request(request: Request) -> tuple[str, str] | tuple[None, None]:
        """Получает access и refresh токены из запроса."""

        try:
            access_token = request.COOKIES['access_token']
            refresh_token = request.COOKIES['refresh_token']
            return access_token, refresh_token

        except KeyError:
            return None, None

    @staticmethod
    def is_expired(token: str | bytes) -> bool:
        """Проверяет, истек ли токен."""

        try:
            JWTService.get_payload(token=token)
            return False

        except jwt.ExpiredSignatureError:
            return True

    @staticmethod
    def get_payload(token: str | bytes) -> dict:
        """Декодирует payload у токена."""

        return jwt.decode(jwt=token, key=settings.JWT_SIGNING_KEY, algorithms=['HS256'])
