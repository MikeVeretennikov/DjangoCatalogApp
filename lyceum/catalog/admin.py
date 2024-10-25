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
    exclude = (models.Item.images.field.name,)


admin.site.register(models.Category)
admin.site.register(models.Tag)


__all__ = []
