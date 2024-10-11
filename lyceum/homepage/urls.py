from django.urls import path

import homepage.views


urlpatterns = [
    path("", homepage.views.index),
    path("coffee/", homepage.views.coffee),
]
