from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, )
    password = serializers.CharField(write_only=True, required=True, label=_('Password'), )


class RegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        label=_('Repeat password'),
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'repeat_password',
        )
        extra_kwargs = {
            'password': {'write_only': True, },
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('repeat_password'):
            raise serializers.ValidationError('Passwords does not match.')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        _ = validated_data.pop('repeat_password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
