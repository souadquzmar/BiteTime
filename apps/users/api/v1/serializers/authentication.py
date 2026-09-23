from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.components.registration import register_customer
from apps.users.models import Role, User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True)
    bio = serializers.CharField(allow_blank=True, required=False)
    avatar = serializers.ImageField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2", "bio", "avatar"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = register_customer(**validated_data)

        return user
