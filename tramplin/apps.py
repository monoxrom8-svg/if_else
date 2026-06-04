from django.apps import AppConfig


class TramplinConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tramplin"
    verbose_name = "Трамплин"

    def ready(self):
        # Регистрируем сигналы приложения
        import tramplin.models  # noqa: F401 — signals are defined at module level
