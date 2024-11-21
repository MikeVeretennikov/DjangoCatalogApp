from django.contrib import admin

import rating.models


@admin.register(rating.models.Rating)
class RatingAdmin(admin.ModelAdmin):
    readonly_fields = (
        rating.models.Rating.user.field.name,
        rating.models.Rating.score.field.name,
        rating.models.Rating.item.field.name,
        rating.models.Rating.created_at.field.name,
        rating.models.Rating.updated_at.field.name,
    )


__all__ = ()
