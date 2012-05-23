from django.core.files.storage import get_storage_class
from cumulus.storage import CloudFilesStaticStorage

class CachedCloudFilesStorage(CloudFilesStaticStorage):
    """
    CloudFiles storage backend that saves the static files locally too.
    Used for django-compresssor.
    """
    def __init__(self, *args, **kwargs):
        super(CachedCloudFilesStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        name = super(CachedCloudFilesStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
