import re

import django.conf
import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.safestring
import sorl.thumbnail
import tinymce
import tinymce.models
import transliterate
import transliterate.exceptions


import catalog.managers
import catalog.models
import catalog.validators
import core.models


ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


def normalize(text):
    try:
        transliterated = transliterate.translit(
            text.lower(),
            reversed=True,
            language_code="ru",
        )
    except transliterate.exceptions.LanguageDetectionError:
        transliterated = text.lower()

    return ONLY_LETTERS_REGEX.sub(
        "",
        transliterated,
    )


class Tag(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="введите слаг",
    )

    normalized_name = django.db.models.CharField(
        "нормализированное имя",
        max_length=150,
        unique=False,
        blank=True,
        default=None,
        null=True,
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
        "слаг",
        max_length=200,
        unique=True,
        help_text="введите слаг",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        "вес",
        default=100,
        validators=[catalog.validators.validate_int_from_1_to_32767],
        help_text="введите вес",
    )

    normalized_name = django.db.models.CharField(
        "нормализированное имя",
        max_length=150,
        unique=False,
        blank=True,
        default=None,
        null=True,
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
    text = tinymce.models.HTMLField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain("роскошно", "превосходно"),
        ],
        help_text="введите текст",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        default=None,
        related_name="items",
        related_query_name="item",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        related_query_name="item",
    )

    is_on_main = django.db.models.BooleanField(
        "принадлежит к главной странице",
        default=False,
        help_text="введите принадлежит ли к главной странице товар",
    )
    created_at = django.db.models.DateTimeField(
        "дата создания",
        auto_now_add=True,
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        "обновлено",
        auto_now=True,
        null=True,
    )

    objects = catalog.managers.ItemManager()

    def image_tmb(self):
        if self.main_image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.main_image.image.url}' width='50'>",
            )

        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class MainImage(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to=django.conf.settings.UPLOAD_TO_PATH,
    )

    item = django.db.models.OneToOneField(
        "Item",
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
        verbose_name="id айтема",
        to_field="id",
        related_name="main_image",
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(self.image, "300", quality=51)

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return self.image.name[:20]


class GalleryImage(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to=django.conf.settings.UPLOAD_TO_PATH,
        default=None,
    )

    item = django.db.models.ForeignKey(
        "Item",
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
        verbose_name="id айтема",
        to_field="id",
        related_name="images",
    )

    class Meta:
        verbose_name = "изображения"
        verbose_name_plural = "изображения"

    def __str__(self):
        return self.image.name[:20]


__all__ = ()
