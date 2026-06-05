import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.deconstruct import deconstructible


def _resource_type(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg"}:
        return "image"
    if ext in {"mp4", "webm", "mov", "avi"}:
        return "video"
    return "raw"


def _public_id(name):
    return name.replace("\\", "/").lstrip("/")


def _configure_cloudinary():
    if not getattr(settings, "CLOUDINARY_CONFIGURED", False):
        return
    if os.environ.get("CLOUDINARY_URL"):
        cloudinary.config(secure=True)
        return
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


@deconstructible
class HybridCloudinaryStorage(Storage):
    """Upload media to Cloudinary; keep serving legacy files from local /media/."""

    def __init__(self):
        self._local = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL,
        )

    def _local_path(self, name):
        return settings.MEDIA_ROOT / _public_id(name)

    def _open(self, name, mode="rb"):
        return self._local.open(_public_id(name), mode)

    def exists(self, name):
        name = _public_id(name)
        if self._local_path(name).exists():
            return True
        _configure_cloudinary()
        try:
            cloudinary.api.resource(name, resource_type=_resource_type(name))
            return True
        except Exception:
            return False

    def url(self, name):
        name = _public_id(name)
        if self._local_path(name).exists():
            return self._local.url(name)
        _configure_cloudinary()
        cloud_id = name.rsplit(".", 1)[0] if "." in name else name
        return cloudinary.utils.cloudinary_url(
            cloud_id,
            secure=True,
            resource_type=_resource_type(name),
        )[0]

    def delete(self, name):
        name = _public_id(name)
        local_path = self._local_path(name)
        if local_path.exists():
            local_path.unlink(missing_ok=True)
        _configure_cloudinary()
        cloud_id = name.rsplit(".", 1)[0] if "." in name else name
        try:
            cloudinary.uploader.destroy(cloud_id, resource_type=_resource_type(name), invalidate=True)
        except Exception:
            pass

    def save(self, name, content, max_length=None):
        name = _public_id(name)
        if self._local_path(name).exists():
            self._local_path(name).unlink(missing_ok=True)

        _configure_cloudinary()
        content.seek(0)
        public_id = name.rsplit(".", 1)[0] if "." in name else name
        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            resource_type=_resource_type(name),
            overwrite=True,
            use_filename=False,
        )
        return result.get("public_id", public_id)

    def size(self, name):
        name = _public_id(name)
        if self._local_path(name).exists():
            return self._local_path(name).stat().st_size
        _configure_cloudinary()
        resource = cloudinary.api.resource(name, resource_type=_resource_type(name))
        return resource.get("bytes", 0)

    def get_available_name(self, name, max_length=None):
        return self._local.get_available_name(_public_id(name), max_length=max_length)
