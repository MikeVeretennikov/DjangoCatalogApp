from django.contrib import admin

from catalog import models


class ImageInline(admin.TabularInline):
    model = models.MainImage


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


@admin.register(models.MainImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = (models.MainImage.image_tmb,)


__all__ = []
