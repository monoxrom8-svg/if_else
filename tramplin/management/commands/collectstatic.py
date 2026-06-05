"""Use Django's collectstatic; cloudinary_storage's override breaks on Django 5."""

from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)


class Command(CollectStaticCommand):
    pass
