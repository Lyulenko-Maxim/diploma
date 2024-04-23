from django.contrib.auth import get_user_model

from src.shared.constants import InvitationType

from ..management.models import WorkspaceMember
from ..management.models import BoardMember

User = get_user_model()


class InvitationMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__type = None
        self.__board = None
        self.__workspace = None
        self.__recipient = None

    def __check_attributes(self):
        required_attributes = ['workspace', 'recipient']
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f'Attribute {attr} is not defined')

        self.__workspace = getattr(self, 'workspace')
        self.__recipient = getattr(self, 'recipient')

    def accept(self):
        from .models import Invitation

        self.__check_attributes()
        WorkspaceMember.objects.create(workspace=self.__workspace, member=self.__recipient)
        Invitation.objects.filter(workspace=self.__workspace, recipient=self.__recipient).delete()

        # if self.__type == InvitationType.BOARD:
        #     BoardMember.objects.create(board=self.__board, member=self.__recipient)
        #     Invitation.objects.filter(board=self.__board, recipient=self.__recipient).delete()
        #
        # if self.__type == InvitationType.WORKSPACE:
        #     WorkspaceMember.objects.create(workspace=self.__workspace, member=self.__recipient)
        #     Invitation.objects.filter(workspace=self.__workspace, recipient=self.__recipient).delete()

    def reject(self):
        from .models import Invitation

        self.__check_attributes()
        Invitation.objects.filter(workspace=self.__workspace, recipient=self.__recipient).delete()
        # if self.__type == InvitationType.WORKSPACE:
        #     Invitation.objects.filter(workspace=self.__workspace, recipient=self.__recipient).delete()
        #
        # if self.__type == InvitationType.BOARD:
        #     Invitation.objects.filter(board=self.__team, recipient=self.__recipient).delete()
