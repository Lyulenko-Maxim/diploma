import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..shared.models import UUIDModel


class User(AbstractBaseUser, PermissionsMixin):
    from .managers import UserManager
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, unique=True, editable=False, )
    email = models.EmailField(_('email address'), unique=True, )
    new_email = models.EmailField(_('new email address'), null=True, blank=True, )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, )
    is_active = models.BooleanField(_('active'), default=False, )
    is_staff = models.BooleanField(_('staff status'), default=False, )
    is_superuser = models.BooleanField(_('superuser status'), default=False, )
    is_verified = models.BooleanField(_('is verified'), default=False, )
    is_deactivated = models.BooleanField(_('deactivated'), default=False, editable=False)
    delete_id = models.UUIDField(_('delete id'), unique=True, null=True, blank=True, editable=False, )
    deleted_at = models.DateTimeField(_('deleted at'), null=True, blank=True, )
    connections = models.PositiveIntegerField(_('connections'), default=0, editable=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'


def profile_photo_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'profiles/{instance.id}/photo.{extension}'


class Profile(UUIDModel):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'), )
    username = models.CharField(_('username'), max_length=32, null=True, blank=True, )
    first_name = models.CharField(_('first name'), max_length=64, blank=True, null=True, )
    last_name = models.CharField(_('last name'), max_length=64, blank=True, null=True, )
    banner_color_hex = models.CharField(_('banner color'), max_length=7, default='#FFF', )
    photo = models.ImageField(
        _('photo'),
        upload_to=profile_photo_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.username:
            return super().save()
        self.username = f'Пользователь #{str(self.id)[:16]}'
        return super().save()


class ProfileSettings(UUIDModel):
    ACCESS_CHOICES = [
        ('all', _('All')),
        ('members', _('Members')),
        ('nobody', _('Nobody')),
    ]

    class Meta:
        verbose_name = _('profile settings')
        verbose_name_plural = _('profile settings')

    email_visibility = models.CharField(_('who can view email'), max_length=10, choices=ACCESS_CHOICES, default='me')
    invitation = models.CharField(_('who can invite'), max_length=10, choices=ACCESS_CHOICES, default='all')

    # avatar = models.OneToOneField('ProfilePhoto', on_delete=models.CASCADE, related_name='related_profile',
    #                               blank=True, null=True, verbose_name='avatar', )

    # class ProfilePhoto(UUIDModel):
    #     class Meta:
    #         verbose_name = _('profile photo')
    #         verbose_name_plural = _('profiles photos')
    #
    #     image = models.ImageField(_('image'), upload_to='', blank=True, null=True, )
    #     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos', verbose_name=_('profile'), )
