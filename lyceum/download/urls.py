from django.urls import path

import download.views


app_name = "download"

urlpatterns = [
    path("", download.views.download_image, name="download"),
]
