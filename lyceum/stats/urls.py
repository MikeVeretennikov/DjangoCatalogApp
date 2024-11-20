from django.urls import path

import stats.views

app_name = "stats"

urlpatterns = [
    path(
        "users/<int:pk>/",
        stats.views.UserDetailView.as_view(),
        name="user-stats-detail",
    ),
    path("rated/", stats.views.RatedItemsView.as_view(), name="rated-items"),
    path(
        "items/<int:pk>/",
        stats.views.ItemDetailView.as_view(),
        name="item-stats-detail",
    ),
]
