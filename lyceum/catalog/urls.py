from django.urls import path, re_path, register_converter

import converters
import views

register_converter(converters.PositiveIntegerConverter, "posint")

urlpatterns = [
    path("", views.item_list),
    re_path(r"^re/(?P<number>0*[1-9][0-9]*)/", views.re_endpoint),
    path("converter/<posint:number>/", views.converter_endpoint),
    path("<int:elem>/", views.item_detail),
]
