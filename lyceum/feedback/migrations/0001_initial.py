# Generated by Django 4.2.16 on 2024-11-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                    "name",
                    models.CharField(max_length=150),
                ),
                (
                    "text",
                    models.TextField(max_length=3000),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        null=True,
                    ),
                ),
                (
                    "mail",
                    models.EmailField(max_length=254),
                ),
            ],
            options={
                "verbose_name": "обратная связь",
            },
        ),
    ]
