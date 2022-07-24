import unicodedata

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION

    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(StaticStorage, self).get_valid_name(name)


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False

    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(PublicMediaStorage, self).get_valid_name(name)


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(PrivateMediaStorage, self).get_valid_name(name)
