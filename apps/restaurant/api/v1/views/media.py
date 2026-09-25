from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.restaurant.api.v1.serializers import PresignedUploadSerializer
from apps.restaurant.models import TemporaryUpload
from apps.restaurant.models.upload import Status
from core.helpers import generate_object_key
from services import StorageService


class PresignedUploadView(generics.GenericAPIView):
    serializer_class = PresignedUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_name = serializer.validated_data["file_name"]
        content_type = serializer.validated_data["content_type"]

        object_key = generate_object_key(file_name)

        expiration = 900
        expires_at = timezone.now() + timedelta(seconds=expiration)

        upload = TemporaryUpload.objects.create(
            user=request.user,
            object_key=object_key,
            content_type=content_type,
            expires_at=expires_at,
        )

        upload_url = StorageService.generate_presigned_upload_url(
            object_key=object_key,
            content_type=content_type,
            expiration=expiration,
        )

        return Response(
            {
                "upload_id": upload.id,
                "upload_url": upload_url,
                "object_key": object_key,
                "expires_at": expires_at,
            }
        )


class CompleteUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, upload_id):

        try:
            upload = TemporaryUpload.objects.get(
                id=upload_id,
                user=request.user,
            )
        except TemporaryUpload.DoesNotExist:
            return Response(
                {"detail": "Upload not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if upload.status != Status.PENDING:
            return Response(
                {"detail": "Upload is no longer pending."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if upload.expires_at <= timezone.now():
            upload.status = Status.EXPIRED
            upload.save(update_fields=["status"])

            return Response(
                {"detail": "Upload has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        upload.status = Status.COMPLETED
        upload.save(update_fields=["status"])

        return Response(
            {
                "upload_id": upload.id,
                "object_key": upload.object_key,
                "status": upload.status,
            },
            status=status.HTTP_200_OK,
        )
