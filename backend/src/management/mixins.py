from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from src.users.models import Profile

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response


class WorkspaceMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__owner = None
        self.__blacklist = None

    def __check_attributes(self):
        required_attributes = ['owner', 'blacklist']
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f'Attribute {attr} is not defined')

        self.__owner = getattr(self, 'owner')
        self.__blacklist = getattr(self, 'blacklist')

    def is_in_blacklist(self, profile):
        self.__check_attributes()
        return self.__blacklist.filter(blocked=profile).exists()

    def invite(self, sender, email: str) -> Response:
        from django.contrib.auth import get_user_model
        from ..notifications.models import Invitation
        from .models import WorkspaceMember

        user = get_user_model().objects.filter(email=email).first()

        if not user:
            return Response({'error': _('User with this email address was not found')},
                            status=status.HTTP_404_NOT_FOUND)

        recipient = user.profile

        if recipient.is_in_blacklist(profile=sender):
            return Response({'error': _('This user no longer accepts invitations from you')},
                            status=status.HTTP_404_NOT_FOUND)

        if Invitation.objects.filter(workspace=self, recipient=recipient).exists():
            return Response({'error': _('This user is already invited to the team')},
                            status=status.HTTP_400_BAD_REQUEST)

        if WorkspaceMember.objects.filter(workspace=self, member=recipient).exists():
            return Response({'error': _('This user is already a member of the team')},
                            status=status.HTTP_400_BAD_REQUEST)

        Invitation.objects.create(workspace=self, sender=sender, recipient=recipient)
        return Response({'success': _('Successfully invited')}, status=status.HTTP_200_OK)

    def expel(self, member) -> Response:
        self.__check_attributes()
        if member == self.__owner:
            return Response({'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

        member.delete()
        return Response({'success': _('Successfully expelled')}, status=status.HTTP_200_OK)


class BoardMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__owner = None

    def __check_attributes(self):
        required_attributes = ['owner', ]
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f'Attribute {attr} is not defined')

        self.__owner = getattr(self, 'owner')

    def invite(self, sender: Profile, email: str) -> Response:
        from ..notifications.models import Invitation
        from src.management.models import BoardMember
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.filter(email=email).first()

        if not user:
            return Response({'error': _('User with this email address was not found')},
                            status=status.HTTP_404_NOT_FOUND)

        recipient = user.profile

        if recipient.is_in_blacklist(profile=sender):
            return Response({'error': _('This user no longer accepts invitations from you')},
                            status=status.HTTP_404_NOT_FOUND)

        if Invitation.objects.filter(board=self, recipient=recipient).exists():
            return Response({'error': _('This user is already invited to this board')},
                            status=status.HTTP_400_BAD_REQUEST)

        if BoardMember.objects.filter(board=self, member=recipient).exists():
            return Response({'error': _('This user is already a member of the board')},
                            status=status.HTTP_400_BAD_REQUEST)

        Invitation.objects.create(board=self, sender=sender, recipient=recipient)
        return Response({'success': _('Successfully invited')}, status=status.HTTP_200_OK)

    def expel(self, member) -> Response:
        self.__check_attributes()
        if member == self.__owner:
            return Response({'error': _('Permission denied')}, status=status.HTTP_403_FORBIDDEN)

        member.delete()
        return Response({'success': _('Successfully expelled')}, status=status.HTTP_200_OK)

# def _is_invite_possible(self, recipient: Profile, hours_limit: int, count_limit: int) \
#          -> tuple[bool, str]:
#
#      from .models import BoardMember
#      from ..notifications.models import Invitation
#
#      if BoardMember.objects.filter(board=self, member=recipient).exists():
#          return False, 'This user is already a member of the board'
#
#      recent_invites_count = Invitation.objects.filter(
#          board=self,
#          recipient=recipient,
#          invited_at__gte=timezone.now() - timezone.timedelta(hours=hours_limit)
#      ).count()
#
#      if recent_invites_count >= count_limit:
#          return False, f'Too many invitations in the last {hours_limit} hours'
#
#      return True, 'Invitation is possible'
#
#  def _invite(self, sender: Profile, email: str, hours_limit: int, count_limit: int) \
#          -> tuple[object | None, str, int]:
#
#      from ..notifications.models import Invitation
#
#      try:
#          user = User.objects.get(email=email)
#          recipient = user.profile
#      except User.DoesNotExist:
#          return None, 'User with this email address was not found', status.HTTP_404_NOT_FOUND
#
#      result, message = self._is_invite_possible(
#          recipient=recipient,
#          hours_limit=hours_limit,
#          count_limit=count_limit
#      )
#
#      if not result:
#          return None, message, status.HTTP_400_BAD_REQUEST
#
#      return (
#          Invitation.objects.create(board=self, sender=sender, recipient=recipient),
#          'Successfully invited',
#          status.HTTP_200_OK
#      )
