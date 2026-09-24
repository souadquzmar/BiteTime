from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.restaurant.api.v1.serializers import PresignedUploadSerializer
from services import StorageService


class PresignedUploadView(generics.GenericAPIView):
    serializer_class = PresignedUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload_url = StorageService.generate_presigned_upload_url(
            object_key=serializer.validated_data["file_name"],
            content_type=serializer.validated_data["content_type"],
        )

        return Response(
            {
                "upload_url": upload_url,
                "file_name": serializer.validated_data["file_name"],
            }
        )
