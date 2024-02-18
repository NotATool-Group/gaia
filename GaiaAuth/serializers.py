from django.conf import settings
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.db import transaction
from rest_framework.serializers import ModelSerializer

from .models import User
from .service import send_activation_email


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["id", "is_staff", "is_active", "is_verified", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}}
        exclude = ["is_staff", "is_active", "is_verified", "date_joined", "last_login"]

    def validate_password(self, value):
        django_validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            is_active=not settings.CONFIRMATION_EMAIL_ENABLED, is_verified=False, **validated_data
        )
        if settings.CONFIRMATION_EMAIL_ENABLED:
            send_activation_email(user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
