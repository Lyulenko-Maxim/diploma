from ..management.models import ProjectMember


class InvitationMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__project = None
        self.__recipient = None

    def __check_attributes(self):
        required_attributes = ['project', 'recipient']
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f'Attribute {attr} is not defined')

        self.__project = getattr(self, 'project')
        self.__recipient = getattr(self, 'recipient')

    def accept(self):
        from .models import Invitation

        self.__check_attributes()
        ProjectMember.objects.create(project=self.__project, profile=self.__recipient)
        Invitation.objects.filter(project=self.__project, recipient=self.__recipient).delete()

    def reject(self):
        from .models import Invitation

        self.__check_attributes()
        Invitation.objects.filter(project=self.__project, recipient=self.__recipient).delete()
