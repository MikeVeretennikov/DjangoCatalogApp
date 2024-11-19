from django.contrib.auth.models import User
from django.db import models

import catalog.models


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="пользователь",
        related_name="ratings",
    )
    item = models.ForeignKey(
        catalog.models.Item,
        on_delete=models.CASCADE,
        help_text="товар",
        related_name="ratings",
    )
    score = models.IntegerField(
        choices=[
            (1, "Ненависть"),
            (2, "Неприязнь"),
            (3, "Нейтрально"),
            (4, "Обожание"),
            (5, "Любовь"),
        ],
        help_text="оценка",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        help_text="дата создания",
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        help_text="дата последнего изменения",
        auto_now=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} оценил {self.item.name} на {self.score}"


__all__ = ()
