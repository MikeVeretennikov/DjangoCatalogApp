from django.urls import path

import homepage.views


urlpatterns = [
    path("", homepage.views.index, name="homepage-index-page"),
    path("coffee/", homepage.views.coffee, name="homepage-coffee-page"),
]
