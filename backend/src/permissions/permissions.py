# from django.contrib.auth import get_user_model
# from rest_framework.permissions import BasePermission, SAFE_METHODS
#
# from src.permissions.models import Group
# from src.shared.constants import Permissions, PrivacyType
# from src.management.models import Board, BoardMember, WorkspaceMember
#
# User = get_user_model()
#
#
# class BoardPermission(BasePermission):
#
#     def has_object_permission(self, request, view, board: Board):
#         if request.user.profile == board.owner:
#             return True
#
#         if board.privacy == PrivacyType.PUBLIC and request.method in SAFE_METHODS:
#             return True
#
#         if board.privacy == PrivacyType.PRIVATE and request.method in SAFE_METHODS:
#             if request.user.profile in board.members:
#                 return True
#
#         if board.privacy == PrivacyType.TEAM and request.method in SAFE_METHODS:
#             if request.user.profile in board.members:
#                 return True
#
#         return False
#
#
# class HasGroupPermission(BasePermission):
#     def has_object_permission(self, request, view, group: Group):
#         workspace = group.workspace
#         profile = request.user.profile
#
#         if profile == workspace.owner:
#             return True
#
#         member = WorkspaceMember.objects.filter(member=profile, workspace=workspace).first()
#
#         if not member:
#             return False
#
#         method = request.method
#
#         if method in SAFE_METHODS:
#             return True
#
#         if method in ('POST',):
#             return True
#
#         if method in ('PUT', 'PATCH',):
#             return True
#
#         if method in ('DELETE',):
#             return True
#
#         return False
#
#
# class CanEditBoardPermission(BasePermission):
#     def has_object_permission(self, request, view, board: Board):
#         if request.user.profile == board.owner:
#             return True
#
#         board_member = BoardMember.objects.filter(member=request.user.profile, board=board).first()
#
#         if board_member:
#             return board_member.has_permission(Permissions.Code.EDIT_BOARD_CODE)
#
#         return False
