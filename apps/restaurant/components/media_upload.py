from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.restaurant.models import TemporaryUpload
from apps.restaurant.models.upload import Status
from core.helpers import generate_object_key
from services import StorageService


class MediaUploadComponent:

    @staticmethod
    def create_presigned_upload(*, user, file_name, content_type):
        object_key = generate_object_key(file_name)

        expiration = 900
        expires_at = timezone.now() + timedelta(
            seconds=expiration
        )

        upload = TemporaryUpload.objects.create(
            user=user,
            object_key=object_key,
            content_type=content_type,
            expires_at=expires_at,
        )

        upload_url = StorageService.generate_presigned_upload_url(
            object_key=object_key,
            content_type=content_type,
            expiration=expiration,
        )

        return upload, upload_url, expires_at

    @staticmethod
    def complete_upload(*, upload):
        if upload.status != Status.PENDING:
            raise ValidationError(
                "Upload is no longer pending."
            )

        if upload.expires_at <= timezone.now():
            upload.status = Status.EXPIRED
            upload.save(update_fields=["status"])

            raise ValidationError(
                "Upload has expired."
            )

        upload.status = Status.COMPLETED
        upload.save(update_fields=["status"])

        return upload