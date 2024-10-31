import django.shortcuts
import django.urls

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"

    items = catalog.models.Item.published.all()


    context = {
        "items": items,
    }
    return django.shortcuts.render(
        request,
        template,
        context,
    )


def item_detail(request, pk):
    template = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.only("name", "text", "category")
        .select_related("category", "main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .prefetch_related("images"),
        pk=pk,
    )
    context = {"item": item}

    return django.shortcuts.render(
        request,
        template,
        context,
    )


__all__ = []
