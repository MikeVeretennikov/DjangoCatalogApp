from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.index, name="index-page"),
    path("coffee/", homepage.views.coffee, name="coffee-page"),
]
