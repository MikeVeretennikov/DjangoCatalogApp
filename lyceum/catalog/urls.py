from django.urls import path

import catalog.converters
import catalog.views


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
        name="item-detail",
    ),
    path(
        "<int:pk>/delete_rating/",
        catalog.views.RatingDeleteView.as_view(),
        name="delete-rating",
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
