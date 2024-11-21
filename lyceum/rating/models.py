from django.contrib.auth.models import User
from django.db import models

import catalog.models


class Rating(models.Model):
    class ScoreChoices(models.IntegerChoices):
        hate = 1, "Ненависть"
        dislike = 2, "Неприязнь"
        normal = 3, "Нейтрально"
        like = 4, "Обожание"
        love = 5, "Любовь"

        __empty__ = "Неизвестно"

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
        choices=ScoreChoices.choices,
        default=ScoreChoices.normal,
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

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "item_id"],
                name="unique_user_item",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} оценил {self.item.name} на {self.score}"


__all__ = ()
