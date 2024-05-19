from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        with transaction.atomic():
            user = self._create_user(email, password, **extra_fields)
            self._initialize(user=user, username=username)
            return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        with transaction.atomic():
            superuser = self._create_user(email, password, **extra_fields)
            self._initialize(user=superuser, username=username)
            return superuser

    @staticmethod
    def _initialize(user, username):
        from .models import Profile
        from ..management.models import Dashboard

        profile, _ = Profile.objects.get_or_create(user=user, username=username)
        dashboard, _ = Dashboard.objects.get_or_create(owner=profile)


class ProfileManager(models.Manager):
    def current(self, request: Request):
        return self.filter(user=request.user).first()
