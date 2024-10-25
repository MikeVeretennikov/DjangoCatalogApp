from django.contrib import admin

from catalog import models


class MainImageInline(admin.TabularInline):
    model = models.MainImage


class GalleryImageInline(admin.TabularInline):
    model = models.GalleryImage


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = [models.Item.name.field.name]
    filter_horizontal = (models.Item.tags.field.name,)
    inlines = [MainImageInline, GalleryImageInline]


admin.site.register(models.Category)
admin.site.register(models.Tag)


__all__ = []
