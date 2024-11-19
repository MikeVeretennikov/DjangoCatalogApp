from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path(
        "",
        homepage.views.HomepageListView.as_view(),
        name="index-page",
    ),
    path(
        "coffee/",
        homepage.views.CoffeeListView.as_view(),
        name="coffee",
    ),
    path(
        "echo/",
        homepage.views.EchoView.as_view(),
        name="echo-page",
    ),
    path(
        "echo/submit/",
        homepage.views.EchoSubmitView.as_view(),
        name="echo-submit-page",
    ),
]
