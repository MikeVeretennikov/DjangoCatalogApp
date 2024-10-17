import django.core.exceptions
import django.core.validators
import django.db.models

import catalog.validators
import core.models


class Tag(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
        verbose_name="слаг",
        help_text="введите слаг",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
        verbose_name="слаг",
        help_text="введите слаг",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        default=100,
        verbose_name="вес",
        validators=[catalog.validators.validate_int_from_1_to_32767],
        help_text="введите вес",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(core.models.AbstractModel):
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[
            catalog.validators.ValidateMustContain("роскошно", "превосходно"),
        ],
        help_text="введите текст",
    )
    category = django.db.models.ForeignKey(
        "category",
        on_delete=django.db.models.CASCADE,
        default=None,
        related_name="catalog_items",
    )
    tags = django.db.models.ManyToManyField(Tag)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
