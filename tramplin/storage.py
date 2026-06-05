import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
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


def _cloud_id(name):
    name = _public_id(name)
    return name.rsplit(".", 1)[0] if "." in name else name


def _file_format(name):
    if "." not in name:
        return None
    ext = name.rsplit(".", 1)[-1].lower()
    return "jpg" if ext == "jpeg" else ext


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


def _cloudinary_delivery_url(name):
    _configure_cloudinary()
    cloud_id = _cloud_id(name)
    options = {
        "secure": True,
        "resource_type": _resource_type(name),
    }
    fmt = _file_format(name)
    if fmt:
        options["format"] = fmt
    return cloudinary.utils.cloudinary_url(cloud_id, **options)[0]


@deconstructible
class HybridCloudinaryStorage(Storage):
    """Upload media to Cloudinary; local /media/ only for dev without Cloudinary."""

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
        if not getattr(settings, "CLOUDINARY_CONFIGURED", False):
            return False
        _configure_cloudinary()
        try:
            cloudinary.api.resource(_cloud_id(name), resource_type=_resource_type(name))
            return True
        except Exception:
            return False

    def url(self, name):
        name = _public_id(name)
        if self._local_path(name).exists():
            return self._local.url(name)
        if getattr(settings, "CLOUDINARY_CONFIGURED", False):
            return _cloudinary_delivery_url(name)
        return self._local.url(name)

    def delete(self, name):
        name = _public_id(name)
        local_path = self._local_path(name)
        if local_path.exists():
            local_path.unlink(missing_ok=True)
        if not getattr(settings, "CLOUDINARY_CONFIGURED", False):
            return
        _configure_cloudinary()
        try:
            cloudinary.uploader.destroy(
                _cloud_id(name),
                resource_type=_resource_type(name),
                invalidate=True,
            )
        except Exception:
            pass

    def save(self, name, content, max_length=None):
        name = _public_id(name)
        if not getattr(settings, "CLOUDINARY_CONFIGURED", False):
            return self._local.save(name, content, max_length=max_length)

        if self._local_path(name).exists():
            self._local_path(name).unlink(missing_ok=True)

        _configure_cloudinary()
        content.seek(0)
        public_id = _cloud_id(name)
        try:
            result = cloudinary.uploader.upload(
                content,
                public_id=public_id,
                resource_type=_resource_type(name),
                overwrite=True,
                use_filename=False,
            )
        except CloudinaryError as exc:
            if settings.DEBUG:
                return self._local.save(name, content, max_length=max_length)
            raise OSError(str(exc)) from exc

        if not result.get("secure_url"):
            if settings.DEBUG:
                content.seek(0)
                return self._local.save(name, content, max_length=max_length)
            raise OSError("Не удалось загрузить файл в Cloudinary.")

        stored_id = result.get("public_id", public_id)
        fmt = result.get("format") or _file_format(name)
        if fmt and not stored_id.endswith(f".{fmt}"):
            return f"{stored_id}.{fmt}"
        return stored_id

    def size(self, name):
        name = _public_id(name)
        if self._local_path(name).exists():
            return self._local_path(name).stat().st_size
        _configure_cloudinary()
        resource = cloudinary.api.resource(_cloud_id(name), resource_type=_resource_type(name))
        return resource.get("bytes", 0)

    def get_available_name(self, name, max_length=None):
        return self._local.get_available_name(_public_id(name), max_length=max_length)
