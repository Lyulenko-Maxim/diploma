from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from core.celery import send_email
from src.authentication.services import JWTService

User = get_user_model()

SEPARATOR = 'SEPARATOR'


def login(user, message, status) -> Response:
    response = Response(data={'message': _(message)}, status=status)
    access_token, refresh_token = JWTService.generate_tokens(user)
    response = set_token_cookies(response, access_token, refresh_token)
    return response


def logout(message, status) -> Response:
    response = Response(data={'message': _(message)}, status=status, )
    response.delete_cookie(key='access_token', )
    response.delete_cookie(key='refresh_token', )
    return response


def get_current_host() -> str:
    try:
        return f'http://{Site.objects.get_current().domain}'
    except Site.DoesNotExist:
        return 'localhost'


def generate_activation_link(user: User) -> str:
    return urlsafe_base64_encode(force_bytes(f'{user.id}{SEPARATOR}{user.email}'))


def check_activation_link(link: str) -> User | None:
    try:
        checking_data = force_str(urlsafe_base64_decode(link))
        user_id, email = checking_data.split(SEPARATOR)
        user = User.objects.get(id=user_id, email=email)
        return None if user.is_verified else user
    except User.DoesNotExist:
        return None


def send_activation_email(user: User):
    activation_link = generate_activation_link(user)
    send_email.delay(
        email=user.email,
        subject='Activation email',
        template_name='activation_email.html',
        context={
            'email': user.email,
            'content_message': 'We are happy that we defined communicate with as!',
            'activation_link': f'{get_current_host()}/api/authentication/activate/{activation_link}/'
        }
    )


def check_credentials(email, password) -> tuple[User, str | None] | tuple[None, str]:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None, 'Invalid credentials'

    if not user.check_password(raw_password=password):
        return None, 'Invalid credentials'

    if not user.is_verified:
        return None, 'Unverified'

    return user, None


def set_token_cookies(response: Response, access_token, refresh_token) -> Response:
    token_max_age = int(settings.JWT_REFRESH_TOKEN_EXP_DAYS) * 24 * 3600
    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=token_max_age)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=token_max_age)
    return response


