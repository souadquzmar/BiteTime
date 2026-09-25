import logging

import boto3
from botocore.exceptions import ClientError

from django.conf import settings

logger = logging.getLogger(__name__)


class StorageService:
    @staticmethod
    def generate_presigned_upload_url(
        *,
        object_key: str,
        content_type: str,
        expiration: int = 900,
    ) -> str:
        client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            response = client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": object_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expiration,
            )
        except ClientError:
            logger.exception("Failed to generate pre-signed upload URL.")
            raise

        return response
