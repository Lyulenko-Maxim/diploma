from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    message = 'Требуется авторизация.'
    code = 401

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous
