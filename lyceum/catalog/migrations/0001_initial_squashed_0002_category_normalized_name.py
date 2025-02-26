# Generated by Django 4.2.16 on 2024-10-17 19:21

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    replaces = [
        ("catalog", "0001_initial"),
        (
            "catalog",
            "0002_category_normalized_name",
        ),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="введите опубликовано ли",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="введите слаг",
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="введите вес",
                        validators=[
                            catalog.validators.validate_int_from_1_to_32767
                        ],
                        verbose_name="вес",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=150,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="введите опубликовано ли",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="введите слаг",
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=150,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="введите опубликовано ли",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="введите текст",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "роскошно",
                                "превосходно",
                            )
                        ],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="catalog_items",
                        to="catalog.category",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(to="catalog.tag"),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
