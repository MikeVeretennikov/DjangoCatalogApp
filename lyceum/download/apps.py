from django.apps import AppConfig


class DownloadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "download"
    verbose_name = "Приложение для скачивания файлов"


__all__ = ()
