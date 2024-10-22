from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.PositiveIntegerConverter, "posint")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="index-page"),
    re_path(
        r"^re/(?P<number>0*[1-9][0-9]*)/",
        catalog.views.regex_endpoint,
        name="re-converter-page",
    ),
    path(
        "converter/<posint:number>/",
        catalog.views.regex_endpoint,
        name="custom-converter-page",
    ),
    path(
        "<int:elem>/",
        catalog.views.item_detail,
        name="default-converter-page",
    ),
]
