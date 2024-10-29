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
]
