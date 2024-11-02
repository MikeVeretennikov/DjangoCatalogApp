from datetime import timedelta

from django.db.models import F
import django.http
import django.shortcuts
import django.urls
from django.utils import timezone

import catalog.models


def item_list(request):
    template = "catalog/new_item_list.html"

    items = catalog.models.Item.objects.published()

    context = {"items": items, "title": "Список товаров"}
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

    context = {"item": item, "title": item.name}

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def friday_items(request):
    template = "catalog/item_list.html"

    friday_items = (
        catalog.models.Item.objects.published()
        .filter(updated_at__week_day=6)
        .order_by("-updated_at")[:5]
    )
    context = {"items": friday_items, "title": "Пятница"}

    return django.shortcuts.render(request, template, context)


def new_items(request):
    week_ago = timezone.now() - timedelta(weeks=1)
    template = "homepage/main.html"
    # потому что иначе полетит правильное разбиение по категориям,
    #  ведь у нас потом идет рандомная сортировка

    new_random_items = (
        catalog.models.Item.objects.published()        
        .filter(created_at__gte=week_ago)
        .order_by("?")[:5]
    )
    context = {"items": new_random_items, "title": "Новинки"}

    return django.shortcuts.render(request, template, context)


def unverified_items(request):
    template = "catalog/item_list.html"

    unverified_items = catalog.models.Item.objects.published().filter(
        created_at=F("updated_at"),
    )
    context = {"items": unverified_items, "title": "Непроверенное"}

    return django.shortcuts.render(request, template, context)


__all__ = []
