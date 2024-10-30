import http

import django.shortcuts

import catalog.models


def index(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.only("name", "text", "category")
        .filter(
            is_on_main=True,
            is_published=True,
            category__is_published=True,
        )
        .select_related("category", "main_image")
        .prefetch_related("tags")
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
