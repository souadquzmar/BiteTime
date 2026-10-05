from django.conf import settings
from django.db import models


class Status(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    EXPIRED = "EXPIRED", "Expired"


class TemporaryUpload(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="temporary_uploads",
    )
    object_key = models.CharField(max_length=500)
    content_type = models.CharField(max_length=100)
    expires_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.object_key
