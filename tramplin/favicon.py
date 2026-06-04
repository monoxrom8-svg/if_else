"""Serve favicon from app static (works without collectstatic on production)."""

from pathlib import Path

from django.http import FileResponse, Http404

_ICON_DIR = Path(__file__).resolve().parent / "static" / "tramplin"


def _serve(name: str, content_type: str):
    path = _ICON_DIR / name
    if not path.is_file():
        raise Http404
    response = FileResponse(path.open("rb"), content_type=content_type)
    response["Cache-Control"] = "public, max-age=604800"
    return response


def favicon_ico(request):
    return _serve("favicon.ico", "image/x-icon")


def favicon_svg(request):
    return _serve("favicon.svg", "image/svg+xml")


def apple_touch_icon(request):
    return _serve("apple-touch-icon.png", "image/png")
