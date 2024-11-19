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


class FridayItemDetailView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published().filter(
        updated_at__week_day=6).order_by("-updated_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пятница"
        return context


class NewItemListView(django.views.generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"
    week_ago = django.utils.timezone.now() - datetime.timedelta(weeks=1)
    queryset = catalog.models.Item.objects.published().filter(
        created_at__gte=week_ago).order_by("?")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новинки"
        return context


class UnverifiedItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published().annotate(
        time_difference=ExpressionWrapper(
            F("updated_at") - F("created_at"),
            output_field=DurationField(),
        ),
    ).filter(time_difference__lte=datetime.timedelta(seconds=1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Непроверенное"
        return context


__all__ = ()
