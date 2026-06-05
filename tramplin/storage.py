from django.conf import settings
from django.core.files.storage import FileSystemStorage

try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
except ImportError:  # pragma: no cover - optional until packages installed
    MediaCloudinaryStorage = None


class HybridCloudinaryStorage(MediaCloudinaryStorage):
    """Cloudinary for new uploads; local /media/ URLs for legacy files on disk."""

    def _local_storage(self):
        return FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)

    def _local_path(self, name):
        return settings.MEDIA_ROOT / name

    def exists(self, name):
        if self._local_path(name).exists():
            return True
        return super().exists(name)

    def url(self, name):
        if self._local_path(name).exists():
            return self._local_storage().url(name)
        return super().url(name)

    def delete(self, name):
        local_path = self._local_path(name)
        if local_path.exists():
            local_path.unlink(missing_ok=True)
        try:
            super().delete(name)
        except Exception:
            pass

    def save(self, name, content, max_length=None):
        saved_name = super().save(name, content, max_length=max_length)
        local_path = self._local_path(saved_name)
        if local_path.exists():
            local_path.unlink(missing_ok=True)
        return saved_name
