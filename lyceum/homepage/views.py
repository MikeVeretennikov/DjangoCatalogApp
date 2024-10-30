import http

import django.shortcuts

import catalog.models


def index(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.only("name", "text", "category", "tags")
        .filter(is_on_main=True)
        .select_related("category")
        .prefetch_related("tags", "main_image")
        .order_by("name")
    )
    context = {"items": items}
    return django.shortcuts.render(
        request,
        template,
        context,
    )


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = []
