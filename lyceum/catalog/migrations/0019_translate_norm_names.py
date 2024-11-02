from django.db import migrations
from catalog.models import normalize


def translate_names(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Tag = apps.get_model("catalog", "Tag")
    for tag in Tag.objects.all():
        tag.normalized_name = normalize(tag.name)
        tag.save()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0017_item_created_at_item_updated_at"),
    ]

    operations = [
        migrations.RunPython(translate_names),
    ]