import re

import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.safestring
import sorl.thumbnail

import catalog.validators
import core.models


def normalize(text):
    text = text.lower()
    first_part = r"(-|\.|,|-|!|\?|\(|\)|\\|%|#|@|^|&|_|\*|\+|"
    second_part = r"\$|\"|'|\;|\:|\[|\]|\{|\}| )"
    pattern = first_part + second_part
    text = re.sub(
        pattern,
        "",
        text,
    )
    new_text = ""
    for char in text:
        if char == "a":
            new_text += "а"
        elif char == "c":
            new_text += "с"
        elif char == "k":
            new_text += "к"
        elif char == "o":
            new_text += "о"
        elif char == "b":
            new_text += "в"
        elif char == "t":
            new_text += "т"
        elif char == "y":
            new_text += "у"
        elif char == "m":
            new_text += "м"
        elif char == "e":
            new_text += "е"
        else:
            new_text += char
    return new_text


class Tag(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
        verbose_name="слаг",
        help_text="введите слаг",
    )

    normalized_name = django.db.models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.normalized_name = normalize(self.name)
        super().save(**kwargs)

    def clean(self):
        if Tag.objects.filter(normalized_name=normalize(self.name)):
            raise django.core.exceptions.ValidationError(
                "Тег с похожим названием уже существует",
            )


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

    normalized_name = django.db.models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.normalized_name = normalize(self.name)
        super().save(**kwargs)

    def clean(self):
        if Category.objects.filter(normalized_name=normalize(self.name)):
            raise django.core.exceptions.ValidationError(
                "Категория с похожим названием уже существует",
            )


class Item(core.models.AbstractModel):
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[
            catalog.validators.ValidateMustContain("роскошно", "превосходно"),
        ],
        help_text="введите текст",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        default=None,
        related_name="catalog_items",
    )
    tags = django.db.models.ManyToManyField(Tag)

    main_image = django.db.models.OneToOneField(
        "MainImage",
        verbose_name="главное изображение",
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
    )

    images = django.db.models.ForeignKey(
        "MainImage",
        on_delete=django.db.models.CASCADE,
        verbose_name="изображения",
        null=True,
        blank=True,
        related_name="images",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class MainImage(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="uploads/",
        verbose_name="изображение",
    )

    item_id = django.db.models.ForeignKey(
        "Item",
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
        verbose_name="id айтема",
        to_field="id",
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(self.image, "300", quality=51)

    def image_tmb(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.image.url}' width='50'>",
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return self.image.name


__all__ = ["normalize", "Tag", "Category", "Item", "MainImage"]
