import django.conf
from django.contrib.auth.models import User
from django.db import models

import catalog.models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(
        help_text="день рождения",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        catalog.models.MainImage,
        help_text="аватарка",
        upload_to=f"{django.conf.settings.UPLOAD_TO_PATH}profile_images/",
        blank=True,
        null=True,
    )
    coffee_count = models.IntegerField(help_text="счетчик кофе", default=0)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return self.user.username


__all__ = []
