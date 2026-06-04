from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tramplin.favicon import apple_touch_icon, favicon_ico, favicon_svg

urlpatterns = [
    path("favicon.ico", favicon_ico),
    path("favicon.svg", favicon_svg),
    path("apple-touch-icon.png", apple_touch_icon),
    path("admin/", admin.site.urls),
    path("", include("tramplin.urls", namespace="tramplin")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
