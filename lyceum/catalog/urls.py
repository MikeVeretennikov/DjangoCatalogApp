from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.item_list),
    re_path(r"^re/(?P<number>[1-9][0-9]*)", views.re_endpoint),
    path("<int:elem>/", views.item_detail),
]
