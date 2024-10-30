import http

import django.db.models
import django.shortcuts

import catalog.models


def index(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.select_related("category", "main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .filter(
            is_on_main=True,
            is_published=True,
            category__is_published=True,
        )
        .only("name", "text", "category__name", "main_image__image")
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
