from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password",
        ]

    def validate_role(self, value):
        request = self.context.get("request")
        if value == "admin" and request.user.role != "admin":
            raise serializers.ValidationError("Only admin can assign admin role")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# JWT Custom Serializer
"""
Validates credentials
Authenticates the user
Generates two tokens
"""
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "role": self.user.role,
        }

        return data