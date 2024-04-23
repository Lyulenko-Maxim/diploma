from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from ..shared.serializers import CurrentProfileDefault
from .models import Profile, ProfilePhoto

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True, label=_('Old password'), )
    new_password = serializers.CharField(max_length=128, write_only=True, required=True, label=_('New password'), )
    new_password_repeat = serializers.CharField(max_length=128, write_only=True, required=True,
                                                label=_('Repeat new password'), )

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_repeat = attrs.get('new_password_repeat')

        if not self.context['request'].user.check_password(raw_password=old_password):
            raise serializers.ValidationError('Invalid old password.')

        if new_password != new_password_repeat:
            raise serializers.ValidationError('New passwords does not match.')

        if new_password == old_password:
            raise serializers.ValidationError('New password must not be the same as old password.')

        return attrs

    # def update(self, instance, validated_data):
    #     _, _ = validated_data.pop('old_password'), validated_data.pop('new_password_repeat')
    #     new_password = validated_data.pop('new_password')
    #     instance.password = make_password(new_password)
    #     instance.save()
    #     return instance
    #
    # def create(self, validated_data):
    #     pass


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, )

    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'last_name',)


class ProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name',)


class ProfilePhotoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = ('id', 'image',)


class ProfilePhotoSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=CurrentProfileDefault())

    class Meta:
        model = ProfilePhoto
        fields = ('id', 'image', 'profile',)
