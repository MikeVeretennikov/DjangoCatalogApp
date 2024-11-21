import django.db

import catalog.models


class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.published()
            .filter(
                is_on_main=True,
            )
            .order_by(
                catalog.models.Item.name.field.name,
            )
        )

    def item_detail_published(self):
        items_published = self.published().select_related(
            catalog.models.Item.main_image.related.name,
        )
        query_set = items_published.prefetch_related(
            catalog.models.Item.images.field.related_query_name(),
        )
        return query_set.only(
            catalog.models.Item.name.field.name,
            catalog.models.Item.text.field.name,
            catalog.models.Item.category.field.name,
            catalog.models.Item.main_image.related.name,
        )

    def published(self):
        item = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )
        item_field_name = catalog.models.Item.category.field.name
        category_field_name = catalog.models.Category.name.field.name
        category_order_by = f"{item_field_name}__{category_field_name}"
        queryset = item.order_by(
            category_order_by,
            catalog.models.Item.name.field.name,
        )
        return queryset.select_related(
            catalog.models.Item.category.field.name,
        ).prefetch_related(
            django.db.models.Prefetch(
                catalog.models.Item.tags.field.name,
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).defer(catalog.models.Tag.is_published.field.name),
            ),
        )


__all__ = ()
