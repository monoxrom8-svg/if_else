from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from tramplin.storage import HybridCloudinaryStorage


class Command(BaseCommand):
    help = "Проверка подключения к Cloudinary (загрузка тестового файла)."

    def handle(self, *args, **options):
        if not settings.CLOUDINARY_CONFIGURED:
            self.stderr.write(self.style.ERROR(
                "Cloudinary не настроен. Задайте CLOUDINARY_URL или "
                "CLOUDINARY_CLOUD_NAME + CLOUDINARY_API_KEY + CLOUDINARY_API_SECRET."
            ))
            return

        storage = HybridCloudinaryStorage()
        payload = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        name = "avatars/_healthcheck.png"

        try:
            stored = storage.save(name, ContentFile(payload, name="healthcheck.png"))
            url = storage.url(stored)
            storage.delete(stored)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Cloudinary upload failed: {exc}"))
            if "Invalid Signature" in str(exc):
                self.stderr.write(
                    "API Secret не совпадает с API Key. "
                    "Скопируйте CLOUDINARY_URL целиком из Cloudinary Console → API Keys."
                )
            return

        self.stdout.write(self.style.SUCCESS("Cloudinary OK"))
        self.stdout.write(f"Sample URL: {url}")
