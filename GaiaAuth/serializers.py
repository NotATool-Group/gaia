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

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(is_active=False, is_verified=False, **validated_data)
        send_activation_email(user)
        return user
