from django.urls import path, include
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from .views import InvitationViewSet, RegisterGCMDeviceView



device_router = DefaultRouter()

device_router.register('devices', GCMDeviceAuthorizedViewSet)

invitation_router = DefaultRouter()
invitation_router.register(r'invitations', InvitationViewSet, basename='invitations')

urlpatterns = [
    path('me/', include(invitation_router.urls)),
    path('', include(device_router.urls)),
    path('register-device/', RegisterGCMDeviceView.as_view()),
]
