# Generated by Django 4.2.16 on 2024-10-31 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0015_alter_category_normalized_name_and_more_squashed_0016_alter_category_normalized_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
