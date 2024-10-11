from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.PositiveIntegerConverter, "posint")

urlpatterns = [
    path("", catalog.views.item_list),
    re_path(r"^re/(?P<number>0*[1-9][0-9]*)/", catalog.views.regex_endpoint),
    path("converter/<posint:number>/", catalog.views.regex_endpoint),
    path("<int:elem>/", catalog.views.item_detail),
]
