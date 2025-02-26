# Generated by Django 4.2.16 on 2024-10-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("catalog", "0005_alter_item_images"),
        ("catalog", "0006_alter_item_images"),
    ]

    dependencies = [
        ("catalog", "0004_alter_item_main_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="catalog.mainimage",
                verbose_name="изобраажения",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="catalog.mainimage",
                verbose_name="изображения",
            ),
        ),
    ]
