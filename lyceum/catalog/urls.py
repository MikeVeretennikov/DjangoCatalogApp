from django.urls import path, register_converter

import catalog.converters
import catalog.views

register_converter(
    catalog.converters.PositiveIntegerConverter,
    "posint",
)

app_name = "catalog"

urlpatterns = [
    path(
        "",
        catalog.views.ItemListView.as_view(),
        name="index-page",
    ),
    path(
        "<int:pk>/",
        catalog.views.ItemDetailView.as_view(),
        name="default-converter-page",
    ),
    path(
        "new/",
        catalog.views.NewItemListView.as_view(),
        name="new-page",
    ),
    path(
        "friday/",
        catalog.views.FridayItemDetailView.as_view(),
        name="friday-page",
    ),
    path(
        "unverified/",
        catalog.views.UnverifiedItemListView.as_view(),
        name="unverified-page",
    ),
]
