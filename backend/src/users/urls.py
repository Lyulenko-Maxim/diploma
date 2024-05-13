from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.users.views import ProfileViewSet, UserViewSet

account_router = DefaultRouter()
account_router.register(r'me', UserViewSet, basename='account')

profile_router = DefaultRouter()
profile_router.register(r'me', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(account_router.urls)),
    path('', include(profile_router.urls)),
]
