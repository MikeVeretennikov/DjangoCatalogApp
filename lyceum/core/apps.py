from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_vfield = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Базовое приложение"


__all__ = []
