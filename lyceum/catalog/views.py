import django.shortcuts
import django.urls

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.only("name", "text", "category", "tags")
        .filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags", "main_image")
        .order_by("category__name")
    )
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
    item = django.shortcuts.get_object_or_404(catalog.models.Item, pk=pk)
    context = {"item": item}

    return django.shortcuts.render(
        request,
        template,
        context,
    )


__all__ = []
