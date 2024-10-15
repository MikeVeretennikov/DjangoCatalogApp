import django.db.models


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="введите опубликовано ли",
    )
    name = django.db.models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="введите название",
    )

    class Meta:
        abstract = True
