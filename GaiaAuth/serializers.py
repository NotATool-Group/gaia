from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["id", "is_staff", "is_active", "is_verified"]
        exclude = ("password",)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
