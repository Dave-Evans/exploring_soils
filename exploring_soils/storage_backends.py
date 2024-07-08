from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class WiscCCPhotoStorage(S3Boto3Storage):
    bucket_name = settings.AWS_WISC_CC_PHOTO_LOCATION
    location = "media/private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
