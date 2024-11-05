from django.urls import path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.PositiveIntegerConverter, "posint")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="index-page"),
    path(
        "<int:pk>/",
        catalog.views.item_detail,
        name="default-converter-page",
    ),
    path("new/", catalog.views.new_items, name="new-page"),
    path("friday/", catalog.views.friday_items, name="friday-page"),
    path(
        "unverified/",
        catalog.views.unverified_items,
        name="unverified-page",
    ),
]
