from rest_framework import serializers

from apps.users.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "avatar", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
