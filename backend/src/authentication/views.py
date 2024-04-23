from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer
from .utils import check_activation_link, check_credentials, login, logout, send_activation_email
from ..users.models import Profile
from ..users.permissions import IsAnonymous

User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymous]

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user)


class ActivateView(APIView):
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        user = check_activation_link(self.kwargs.get('token'))

        if not user:
            return Response({'error': 'Invalid activation link'}, status=404)

        user.is_active = True
        user.is_verified = True
        user.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        return login(user=user, message='Successful account activation', status=status.HTTP_200_OK)


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
            raise AuthenticationFailed(_(error_message))

        return login(user=user, message='Successful login', status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return logout(message='Successful logout', status=status.HTTP_200_OK)
