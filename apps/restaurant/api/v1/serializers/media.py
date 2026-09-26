from rest_framework import serializers


class PresignedUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    content_type = serializers.CharField()
