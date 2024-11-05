from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.index, name="index-page"),
    path("coffee/", homepage.views.coffee, name="coffee-page"),
    path("echo/", homepage.views.echo, name="echo-page"),
    path("echo/submit/", homepage.views.echo_submit, name="echo-submit-page"),
]
