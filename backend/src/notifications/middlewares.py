import os

import django
import jwt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from urllib.parse import parse_qs
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from src.authentication.services import JWTService

User = get_user_model()


@database_sync_to_async
def get_user(access_token, refresh_token):
    try:
        access_token_payload = JWTService.get_payload(access_token)
        user_id = access_token_payload['id']
        user_email = access_token_payload['email']
        user = User.objects.get(id=user_id, email=user_email)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist, KeyError) as e:
        print(e)

    try:
        refresh_token_payload = JWTService.get_payload(refresh_token)
        user_id = refresh_token_payload['id']
        user_email = refresh_token_payload['email']
        user = User.objects.get(id=user_id, email=user_email)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist, KeyError) as e:
        print(e)

    return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        qs = parse_qs(scope["query_string"].decode("utf8"))
        access_token, refresh_token = qs.get("access_token")[0], qs.get("refresh_token")[0]
        scope["user"] = await get_user(access_token=access_token, refresh_token=refresh_token)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return AuthMiddlewareStack(JwtAuthMiddleware(inner))
