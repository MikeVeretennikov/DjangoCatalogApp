import datetime

from django.db.models import (
    DurationField,
    ExpressionWrapper,
    F,
)
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.views.generic

import catalog.managers
import catalog.models


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Товар детально"
        return context


def friday_items(request):
    template = "catalog/item_list.html"

    published_items = catalog.models.Item.objects.published()
    friday_items = published_items.filter(updated_at__week_day=6).order_by(
        "-updated_at",
    )[:5]
    context = {
        "items": friday_items,
        "title": "Пятница",
    }

    return django.shortcuts.render(request, template, context)


def new_items(request):
    week_ago = django.utils.timezone.now() - datetime.timedelta(weeks=1)
    template = "homepage/main.html"
    # потому что иначе полетит правильное разбиение по категориям,
    #  ведь у нас потом идет рандомная сортировка

    published_items = catalog.models.Item.objects.published()
    new_random_items = published_items.filter(
        created_at__gte=week_ago,
    ).order_by("?")[:5]
    context = {
        "items": new_random_items,
        "title": "Новинки",
    }

    return django.shortcuts.render(request, template, context)


def unverified_items(request):
    template = "catalog/item_list.html"

    published_items = catalog.models.Item.objects.published()
    unverified_items = published_items.annotate(
        time_difference=ExpressionWrapper(
            F("updated_at") - F("created_at"),
            output_field=DurationField(),
        ),
    ).filter(time_difference__lte=datetime.timedelta(seconds=1))

    context = {
        "items": unverified_items,
        "title": "Непроверенное",
    }

    return django.shortcuts.render(request, template, context)


__all__ = ()
