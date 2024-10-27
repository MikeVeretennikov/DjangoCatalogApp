# Generated by Django 4.2.16 on 2024-10-27 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_alter_item_text_squashed_0009_galleryimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainimage",
            name="item",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="main_image",
                to="catalog.item",
                verbose_name="id айтема",
            ),
        ),
    ]
