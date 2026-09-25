from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.restaurant.api.v1.serializers import PresignedUploadSerializer
from apps.restaurant.components import MediaUploadComponent
from apps.restaurant.models import TemporaryUpload


class PresignedUploadView(generics.GenericAPIView):
    serializer_class = PresignedUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload, upload_url, expires_at = MediaUploadComponent.create_presigned_upload(
            user=request.user,
            file_name=serializer.validated_data["file_name"],
            content_type=serializer.validated_data["content_type"],
        )

        return Response(
            {
                "upload_id": upload.id,
                "upload_url": upload_url,
                "object_key": upload.object_key,
                "expires_at": expires_at,
            },
            status=status.HTTP_201_CREATED,
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
            raise NotFound("Upload not found.")

        try:
            upload = MediaUploadComponent.complete_upload(
                upload=upload,
            )
        except ValidationError as exc:
            raise ValidationError(str(exc))

        return Response(
            {
                "upload_id": upload.id,
                "object_key": upload.object_key,
                "status": upload.status,
            },
            status=status.HTTP_200_OK,
        )
