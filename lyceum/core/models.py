import django.db.models


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="введите опубликовано ли",
    )
    name = django.db.models.CharField(
        max_length=150, verbose_name="Название", help_text="введите название"
    )

    class Meta:
        abstract = True
