# Generated by Django 4.2.16 on 2024-10-15 19:21

import catalog.models
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0004_alter_tag_options_alter_category_is_published_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
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
        migrations.AlterField(
            model_name="category",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=100,
                help_text="введите вес",
                validators=[catalog.models.validate_int_from_1_to_32767],
                verbose_name="вес",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="введите текст",
                validators=[catalog.models.validate_perfect_in_text],
                verbose_name="текст",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
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
    ]
