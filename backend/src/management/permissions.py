from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

from src.shared.constants import Permissions, PrivacyType
from src.management.models import Board, BoardMember

User = get_user_model()


class BoardPermission(BasePermission):

    def has_object_permission(self, request, view, board: Board):
        if request.user.profile == board.owner:
            return True

        if board.privacy == PrivacyType.PUBLIC and request.method in SAFE_METHODS:
            return True

        if board.privacy == PrivacyType.PRIVATE and request.method in SAFE_METHODS:
            if request.user.profile in board.members:
                return True

        if board.privacy == PrivacyType.TEAM and request.method in SAFE_METHODS:
            if request.user.profile in board.members:
                return True

        return False


class CanEditBoardPermission(BasePermission):
    def has_object_permission(self, request, view, board: Board):
        if request.user.profile == board.owner:
            return True

        board_member = BoardMember.objects.filter(member=request.user.profile, board=board).first()

        if board_member:
            return board_member.has_permission(Permissions.Code.EDIT_BOARD_CODE)

        return False
