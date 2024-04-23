from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InvitationViewSet

invitation_router = DefaultRouter()
invitation_router.register(r'invitations', InvitationViewSet, basename='invitations')

urlpatterns = [
    path('me/', include(invitation_router.urls)),
]
