import django.contrib.auth.models
import django.db.models


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("received", "получено"),
        ("in_process", "в обработке"),
        ("replied", "ответ дан"),
    ]

    name = django.db.models.CharField(max_length=150, blank=True, null=True)
    text = django.db.models.TextField(max_length=3000)
    created_on = django.db.models.DateTimeField(auto_now_add=True, null=True)
    mail = django.db.models.EmailField(max_length=254)
    status = django.db.models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="received",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"

    def __str__(self):
        return (
            f"Обратная связь пользователи {self.name}, статус: {self.status}"
        )


class StatusLog(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name="status_logs",
        on_delete=django.contrib.auth.models.models.CASCADE,
    )
    user = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=django.contrib.auth.models.models.CASCADE,
    )
    timestamp = django.db.models.DateTimeField(auto_now_add=True)
    from_status = django.db.models.CharField(max_length=20)
    to_status = django.db.models.CharField(max_length=20)

    class Meta:
        verbose_name = "статус лог"
        verbose_name_plural = "статус логи"

    def __str__(self):
        return (
            f"{self.feedback}.\n статус изменился с {self.from_status} "
            f"на {self.to_status} пользователем {self.user}"
        )


__all__ = []
