from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.users.views import ProfileViewSet,UserViewSet

account_router = DefaultRouter()
account_router.register(r'', UserViewSet, basename='')

profile_router = DefaultRouter()
profile_router.register(r'profile', ProfileViewSet, basename='profile')

# team_router = DefaultRouter()
# team_router.register(r'teams', TeamViewSet, basename='teams')
#
# team_member_router = DefaultRouter()
# team_member_router.register(r'members', TeamMemberViewSet, basename='members')

urlpatterns = [
    path('me/', include(account_router.urls)),
    path('me/', include(profile_router.urls)),
    # path('me/', include(team_router.urls)),
    # path('me/teams/<uuid:team_pk>/', include(team_member_router.urls)),
]
