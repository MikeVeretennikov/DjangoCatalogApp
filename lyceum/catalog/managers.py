import django.db

import catalog.models


class ItemManager(django.db.models.Manager):
    def published(self):
        prefetched_queryset = (
            self.get_queryset()
            .filter(
                category__is_published=True,
                is_published=True,
            )
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only("name"),
                ),
            )
        )
        return prefetched_queryset.only(
            "name",
            "category__name",
            "main_image__image",
            "text",
        ).order_by("category__name", "name")

    def on_main(self):
        prefetched_queryset = (
            self.get_queryset()
            .filter(
                is_on_main=True,
                category__is_published=True,
                is_published=True,
            )
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only("name"),
                ),
            )
        )
        return prefetched_queryset.only(
            "name",
            "category__name",
            "main_image__image",
            "text",
        ).order_by("name")


__all__ = []
