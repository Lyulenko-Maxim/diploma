import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'


class Profile(UUIDModel):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'), )
    first_name = models.CharField(_('first name'), max_length=64, blank=True, null=True, )
    last_name = models.CharField(_('last name'), max_length=64, blank=True, null=True, )
    avatar = models.OneToOneField('ProfilePhoto', on_delete=models.CASCADE, related_name='related_profile',
                                  blank=True, null=True, verbose_name='avatar', )


class ProfilePhoto(UUIDModel):
    class Meta:
        verbose_name = _('profile photo')
        verbose_name_plural = _('profiles photos')

    image = models.ImageField(_('image'), upload_to='', blank=True, null=True, )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos', verbose_name=_('profile'), )
