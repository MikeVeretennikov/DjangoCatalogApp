from django.contrib import admin

from catalog import models


class ImageInline(admin.TabularInline):
    model = models.Image


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = [models.Item.name.field.name]
    filter_horizontal = (models.Item.tags.field.name,)
    inlines = [ImageInline]


admin.site.register(models.Category)
admin.site.register(models.Tag)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (models.Image.image_tmb,)


__all__ = ["ImageInline", "ItemAdmin", "ImageAdmin"]
