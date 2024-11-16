import time

import django.conf
import django.contrib.auth.models
import django.db.models


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("received", "получено"),
        ("in_process", "в обработке"),
        ("replied", "ответ дан"),
    ]

    text = django.db.models.TextField(
        max_length=3000,
        help_text="Что вы хотели сообщить?",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
        help_text="время создания",
        null=True,
    )
    status = django.db.models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text="статус фидбека",
        default="received",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"


class FeedbackAuthor(django.db.models.Model):
    feedback = django.db.models.OneToOneField(
        Feedback,
        related_name="author",
        on_delete=django.db.models.CASCADE,
    )
    name = django.db.models.CharField(
        help_text="имя",
        max_length=150,
        null=True,
        blank=True,
    )
    mail = django.db.models.EmailField(help_text="почта", max_length=150)


class FeedbackFile(django.db.models.Model):
    def get_upload_path(self, filename):
        return (
            f"{django.conf.settings.UPLOAD_TO_PATH}"
            f"{self.feedback_id}/{time.time()}_{filename}"
        )

    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name="files",
        on_delete=django.db.models.CASCADE,
    )
    file = django.db.models.FileField(
        help_text="файл",
        upload_to=get_upload_path,
        blank=True,
    )


class StatusLog(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name="status_logs",
        on_delete=django.contrib.auth.models.models.CASCADE,
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.contrib.auth.models.models.CASCADE,
    )
    timestamp = django.db.models.DateTimeField(auto_now_add=True)
    from_status = django.db.models.CharField(max_length=20, db_column="from")
    to = django.db.models.CharField(max_length=20, db_column="to")

    class Meta:
        verbose_name = "статус лог"
        verbose_name_plural = "статус логи"

    def __str__(self):
        return (
            f"{self.feedback}.\n статус изменился с {self.from_status} "
            f"на {self.to_status} пользователем {self.user}"
        )


__all__ = ()
