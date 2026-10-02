from celery import shared_task
from django.utils import timezone

from apps.restaurant.models import TemporaryUpload
from apps.restaurant.models.upload import Status
from services import StorageService


@shared_task
def daily_system_cleanup():
    now = timezone.now()

    uploads = TemporaryUpload.objects.filter(
        status=Status.PENDING,
        expires_at__lte=now,
    )

    deleted_count = 0

    for upload in uploads:
        StorageService.delete_object(
            object_key=upload.object_key,
        )

        upload.status = Status.EXPIRED
        upload.save(update_fields=["status"])

        deleted_count += 1

    return {"deleted_objects": deleted_count}
